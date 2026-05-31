import asyncio
import logging
import os
import tempfile
from datetime import date as DateType, datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, or_, select

from app.core.config import settings
from app.db.session import get_db
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.transcript import Segment, TokenMapRecord, Transkript, FormatTip, TranskStatusTip
from app.db.models.knowledge import UnosBazeZnanja
from app.api.v1.deps import require_role
from app.schemas.transcript import (
    AudioTranscriptConfirm,
    DriveFileStatus,
    DriveImportRequest,
    DriveImportResponse,
    TranscribePreviewResponse,
    TranscriptDetail,
    TranscriptBulkDelete,
    TranscriptManualCreate,
    TranscriptManualResponse,
    TranscriptRead,
    TranscriptUpdate,
    TranscriptUploadResponse,
)
from app.services.storage.storage_service import StorageService
from app.services.transcript.file_utils import (
    MAX_FILE_SIZE,
    classify_file,
    extract_pdf_text,
)
from app.tasks.transcript_tasks import import_drive_folder, process_transcript, purge_transcript, _parse_drive_naziv

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


@router.post("/transcribe-preview", response_model=TranscribePreviewResponse)
async def transcribe_audio_preview(
    file: UploadFile = File(...),
    language: str = Form("bs"),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    from app.services.transcript.transcription_service import TranscriptionService

    is_audio, _, _ = classify_file(file.content_type or "", file.filename or "")
    if not is_audio:
        raise HTTPException(
            status_code=400,
            detail="Only audio files are supported (.mp3, .wav, .m4a, .ogg)",
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Audio file appears to be empty or corrupted")
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds the 10 MB size limit")

    suffix = os.path.splitext(file.filename or ".audio")[1] or ".audio"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            text = TranscriptionService().transcribe(tmp_path, language=language)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"Transcription failed: {type(exc).__name__}: {exc}")
            raise HTTPException(
                status_code=422,
                detail=f"Transcription failed: {type(exc).__name__}: {exc}",
            ) from exc
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="No speech detected in the audio file")

    quality_warning: str | None = None
    chars_per_kb = len(text.strip()) / max(len(file_bytes) / 1024, 1)
    if chars_per_kb < 0.5 and len(file_bytes) > 50 * 1024:
        quality_warning = (
            "Audio quality appears to be low. "
            "The transcription may be incomplete or inaccurate. "
            "Please review carefully before saving."
        )

    return TranscribePreviewResponse(
        text=text.strip(),
        quality_warning=quality_warning,
        filename=file.filename or "audio",
    )


@router.post("/confirm-audio", response_model=TranscriptManualResponse)
async def confirm_audio_transcript(
    body: AudioTranscriptConfirm,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    from app.services.preprocessing.pipeline import run_pipeline

    transkript = Transkript(
        id_korisnika_upload=current_user.id,
        naziv=body.filename,
        file_path=None,
        format=FormatTip.audio,
        raw_text=body.text,
        jezik=body.language,
        status=TranskStatusTip.sirovi,
    )
    db.add(transkript)
    await db.commit()
    await db.refresh(transkript)

    pipeline_result = await run_pipeline(transkript.id, body.text, db)
    transkript.processed_text = pipeline_result.masked_text
    transkript.status = TranskStatusTip.obradjeno
    await db.commit()

    # Embed the freshly-extracted Q&A so the chatbot can use them right away.
    from app.services.ai.kb_indexing import embed_pending
    await embed_pending()

    return TranscriptManualResponse(
        transcript_id=transkript.id,
        message=(
            f"Audio transcript saved successfully. "
            f"{pipeline_result.qa_pair_count} Q&A pair(s) extracted and queued for review."
        ),
    )


@router.post("/upload", response_model=TranscriptUploadResponse)
async def upload_transcript(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    is_audio, is_text, is_pdf = classify_file(
        file.content_type or "", file.filename or ""
    )

    if not (is_audio or is_text or is_pdf):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{file.content_type}'. "
                "Accepted: .txt, .pdf, .mp3, .wav, .m4a, .ogg"
            ),
        )

    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds the 10 MB size limit")

    safe_name = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{file.filename}"

    raw_text: str | None = None
    storage_path: str | None = None

    if is_audio:
        storage = StorageService()
        try:
            storage_path = storage.upload(
                path=safe_name,
                data=file_bytes,
                content_type=file.content_type or "application/octet-stream",
            )
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Storage upload failed: {exc}")
    else:
        if is_text:
            raw_text = file_bytes.decode("utf-8", errors="replace")
        elif is_pdf:
            raw_text = extract_pdf_text(file_bytes)

    transkript = Transkript(
        id_korisnika_upload=current_user.id,
        naziv=file.filename,
        file_path=storage_path,
        format=FormatTip.audio if is_audio else FormatTip.tekst,
        raw_text=raw_text,
        status=TranskStatusTip.sirovi,
    )
    db.add(transkript)
    await db.commit()
    await db.refresh(transkript)

    background_tasks.add_task(process_transcript, transkript.id)

    return TranscriptUploadResponse(
        transcript_id=transkript.id,
        task_id=None,
        message="Upload successful. Processing started.",
    )


@router.post("/import-drive", response_model=DriveImportResponse)
async def import_drive_transcripts(
    body: DriveImportRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise HTTPException(
            status_code=503,
            detail="Google Drive import is not configured (GOOGLE_SERVICE_ACCOUNT_JSON).",
        )

    # The one-click run button sends no folder → fall back to the configured default.
    folder_id = body.folder_id or settings.GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID
    if not folder_id:
        raise HTTPException(
            status_code=400,
            detail="No Drive folder specified and GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID is not set.",
        )

    from app.services.storage.google_drive_service import GoogleDriveService

    try:
        drive_files = GoogleDriveService().list_files(folder_id)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not access the Drive folder. Check the folder ID and sharing: {exc}",
        )

    existing = await db.execute(
        select(Transkript.naziv).where(Transkript.naziv.like(f"gdrive:{folder_id}:%"))
    )
    # file name -> recorded modifiedTime (None for legacy entries without a version)
    recorded: dict[str, str | None] = {}
    for nz in existing.scalars().all():
        parsed = _parse_drive_naziv(nz, folder_id)
        if parsed:
            recorded[parsed[0]] = parsed[1]

    files: list[DriveFileStatus] = []
    new_count = 0
    for f in drive_files:
        name = f["name"]
        # Skip only if this exact version was already imported; a newer
        # modifiedTime (or a legacy entry) is re-imported by the task.
        already = name in recorded and recorded[name] is not None and recorded[name] == f.get("modifiedTime")
        files.append(DriveFileStatus(name=name, status="skipped" if already else "queued"))
        if not already:
            new_count += 1

    language = None if body.language == "auto" else body.language
    background_tasks.add_task(import_drive_folder, folder_id, current_user.id, language)

    if not files:
        message = "No supported files (.mp3, .wav, .m4a, .ogg, .txt, .pdf) found in the folder."
    else:
        message = (
            f"Import started: {new_count} new file(s) queued, "
            f"{len(files) - new_count} already imported."
        )

    return DriveImportResponse(folder_id=folder_id, message=message, files=files)


@router.get("/drive-folder")
async def drive_folder_info(
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    """Name of the configured default Drive folder, shown in the Pipeline view."""
    folder_id = settings.GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID
    if not folder_id or not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        return {"folder_id": folder_id or None, "name": None}
    from app.services.storage.google_drive_service import GoogleDriveService

    try:
        name = await asyncio.to_thread(GoogleDriveService().get_folder_name, folder_id)
    except Exception:
        name = None
    return {"folder_id": folder_id, "name": name}


@router.post("/manual", response_model=TranscriptManualResponse)
async def create_manual_transcript(
    body: TranscriptManualCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    from app.services.preprocessing.pipeline import run_pipeline

    transkript = Transkript(
        id_korisnika_upload=current_user.id,
        naziv=f"manual_{body.agent_name.replace(' ', '_')}_{body.date}.txt",
        file_path=None,
        format=FormatTip.tekst,
        raw_text=body.content,
        status=TranskStatusTip.sirovi,
    )
    db.add(transkript)
    await db.commit()
    await db.refresh(transkript)

    pipeline_result = await run_pipeline(transkript.id, body.content, db)
    transkript.processed_text = pipeline_result.masked_text
    transkript.status = TranskStatusTip.obradjeno
    await db.commit()

    # Embed the freshly-extracted Q&A so the chatbot can use them right away.
    from app.services.ai.kb_indexing import embed_pending
    await embed_pending()

    return TranscriptManualResponse(
        transcript_id=transkript.id,
        message=(
            f"Transcript saved successfully. "
            f"{pipeline_result.qa_pair_count} Q&A pair(s) extracted and queued for review."
        ),
    )


@router.get("/", response_model=list[TranscriptRead])
async def list_transcripts(
    q: Optional[str] = None,
    date_from: Optional[DateType] = None,
    date_to: Optional[DateType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    stmt = select(Transkript).order_by(Transkript.datum_uploada.desc())
    if q:
        term = f"%{q}%"
        stmt = stmt.where(
            or_(
                Transkript.naziv.ilike(term),
                Transkript.raw_text.ilike(term),
                Transkript.processed_text.ilike(term),
            )
        )
    if date_from:
        stmt = stmt.where(
            Transkript.datum_uploada >= datetime.combine(date_from, datetime.min.time())
        )
    if date_to:
        stmt = stmt.where(
            Transkript.datum_uploada < datetime.combine(date_to + timedelta(days=1), datetime.min.time())
        )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/active", response_model=list[TranscriptRead])
async def list_active_transcripts(
    folder_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    """In-progress transcripts only — what the pipeline-progress pollers hit.

    Lightweight: filters to rows still being processed (queued or mid-stage) so an idle
    pipeline returns an empty list instead of the full transcript history.
    """
    stmt = select(Transkript).where(
        or_(
            Transkript.status == TranskStatusTip.sirovi,
            Transkript.pipeline_stage.isnot(None),
        )
    ).order_by(Transkript.datum_uploada.desc())
    if folder_id:
        # Prefix match (index-friendly) — Drive imports are named gdrive:<folder>:<file>.
        stmt = stmt.where(Transkript.naziv.like(f"gdrive:{folder_id}:%"))
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{transcript_id}", response_model=TranscriptDetail)
async def get_transcript(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    result = await db.execute(
        select(Transkript).where(Transkript.id == transcript_id)
    )
    transkript = result.scalar_one_or_none()
    if not transkript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return transkript


@router.patch("/{transcript_id}", response_model=TranscriptDetail)
async def update_transcript(
    transcript_id: int,
    payload: TranscriptUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    result = await db.execute(select(Transkript).where(Transkript.id == transcript_id))
    transkript = result.scalar_one_or_none()
    if not transkript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    if payload.naziv is not None:
        stripped = payload.naziv.strip()
        if stripped:
            transkript.naziv = stripped
    if payload.processed_text is not None:
        transkript.processed_text = payload.processed_text
    await db.commit()
    await db.refresh(transkript)
    return transkript


@router.post("/bulk-delete")
async def bulk_delete_transcripts(
    payload: TranscriptBulkDelete,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    """Delete the given transcripts (and all derived segments / KB entries / vectors)
    in one request. Mirrors the single DELETE cleanup via purge_transcript."""
    if not payload.ids:
        return {"ok": True, "deleted": 0}

    existing = (
        await db.execute(select(Transkript.id).where(Transkript.id.in_(payload.ids)))
    ).scalars().all()
    for tid in existing:
        await purge_transcript(db, tid)
    await db.commit()
    return {"ok": True, "deleted": len(existing)}


@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transcript(
    transcript_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(Transkript).where(Transkript.id == transcript_id))
    transkript = result.scalar_one_or_none()
    if not transkript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    # Clean up children first — segment.id_transkripta has no ON DELETE CASCADE, so a
    # processed transcript (with segments / KB entries / token map) can't be deleted directly.
    seg_ids = (
        await db.execute(select(Segment.id).where(Segment.id_transkripta == transcript_id))
    ).scalars().all()

    if seg_ids:
        kb_entries = (
            await db.execute(
                select(UnosBazeZnanja).where(UnosBazeZnanja.id_segmenta.in_(seg_ids))
            )
        ).scalars().all()
        if kb_entries:
            from app.services.ai.vector_store import get_vector_store

            vector_store = get_vector_store()
            for entry in kb_entries:
                if entry.vector_id:
                    try:
                        vector_store.delete_item(entry.vector_id)
                    except Exception:
                        logger.warning(
                            "Could not delete Qdrant vector %s for KB entry %s",
                            entry.vector_id, entry.id,
                        )
            await db.execute(
                delete(UnosBazeZnanja).where(UnosBazeZnanja.id_segmenta.in_(seg_ids))
            )

    await db.execute(delete(TokenMapRecord).where(TokenMapRecord.transkript_id == transcript_id))
    await db.execute(delete(Segment).where(Segment.id_transkripta == transcript_id))
    await db.delete(transkript)
    await db.commit()
