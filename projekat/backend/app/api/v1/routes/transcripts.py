import io
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.transcript import Transkript, FormatTip, TranskStatusTip
from app.api.v1.deps import require_role
from app.schemas.transcript import (
    TranscriptDetail,
    TranscriptManualCreate,
    TranscriptManualResponse,
    TranscriptRead,
    TranscriptUploadResponse,
)
from app.services.storage.storage_service import StorageService
from app.tasks.transcript_tasks import process_transcript

router = APIRouter(prefix="/transcripts", tags=["transcripts"])

ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a", "audio/ogg"}
ALLOWED_TEXT_TYPES = {"text/plain", "text/x-plain"}
ALLOWED_PDF_TYPES = {"application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _classify_file(content_type: str, filename: str) -> tuple[bool, bool, bool]:
    ct = content_type.lower()
    is_audio = ct in ALLOWED_AUDIO_TYPES
    is_text = ct in ALLOWED_TEXT_TYPES
    is_pdf = ct in ALLOWED_PDF_TYPES

    if not (is_audio or is_text or is_pdf):
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext == "pdf":
            is_pdf = True
        elif ext == "txt":
            is_text = True
        elif ext in {"mp3", "wav", "m4a", "ogg"}:
            is_audio = True

    return is_audio, is_text, is_pdf


def _extract_pdf_text(content: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not extract text from PDF: {exc}")


@router.post("/upload", response_model=TranscriptUploadResponse)
async def upload_transcript(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    is_audio, is_text, is_pdf = _classify_file(
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
            raw_text = _extract_pdf_text(file_bytes)

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


@router.post("/manual", response_model=TranscriptManualResponse)
async def create_manual_transcript(
    body: TranscriptManualCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    from app.services.pipeline.pipeline_service import PipelineService
    from app.db.models.knowledge import UnosBazeZnanja

    pipeline = PipelineService()
    result = pipeline.process(body.content)

    transkript = Transkript(
        id_korisnika_upload=current_user.id,
        naziv=f"manual_{body.agent_name.replace(' ', '_')}_{body.date}.txt",
        file_path=None,
        format=FormatTip.tekst,
        raw_text=body.content,
        processed_text=result.masked_text,
        status=TranskStatusTip.obradjeno,
    )
    db.add(transkript)
    await db.commit()
    await db.refresh(transkript)

    for pair in result.qa_pairs:
        db.add(UnosBazeZnanja(
            pitanje=pair["question"],
            odgovor=pair["answer"],
            status_aprovacije="NaCekanju",
        ))
    await db.commit()

    return TranscriptManualResponse(
        transcript_id=transkript.id,
        message=(
            f"Transcript saved successfully. "
            f"{len(result.qa_pairs)} Q&A pair(s) extracted and queued for review."
        ),
    )


@router.get("/", response_model=list[TranscriptRead])
async def list_transcripts(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)),
):
    result = await db.execute(select(Transkript).order_by(Transkript.datum_uploada.desc()))
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
