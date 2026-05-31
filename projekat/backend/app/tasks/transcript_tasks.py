import logging
import os
import tempfile
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Drive imports are named ``gdrive:<folder_id>:<name>`` with the file's Drive
# modifiedTime appended after this separator, so a re-uploaded/edited file
# (same name, newer modifiedTime) is detected as a new version rather than skipped.
_DRIVE_VER_SEP = "::v::"


def _drive_naziv(folder_id: str, name: str, modified_time: str | None) -> str:
    base = f"gdrive:{folder_id}:{name}"
    return f"{base}{_DRIVE_VER_SEP}{modified_time}" if modified_time else base


def _parse_drive_naziv(naziv: str, folder_id: str) -> tuple[str, str | None] | None:
    """Split a stored naziv into (file_name, modified_time). modified_time is None
    for legacy entries imported before versioning. Returns None if not from this folder."""
    prefix = f"gdrive:{folder_id}:"
    if not naziv.startswith(prefix):
        return None
    rest = naziv[len(prefix):]
    if _DRIVE_VER_SEP in rest:
        name, mtime = rest.rsplit(_DRIVE_VER_SEP, 1)
        return name, mtime
    return rest, None


async def purge_transcript(db, transcript_id: int) -> None:
    """Delete a transcript and all derived data (segments, KB entries, Qdrant vectors,
    token map). Mirrors the cleanup in the DELETE /transcripts route. Does not commit."""
    from sqlalchemy import delete, select

    from app.db.models.transcript import Segment, TokenMapRecord, Transkript
    from app.db.models.knowledge import UnosBazeZnanja

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
    await db.execute(delete(Transkript).where(Transkript.id == transcript_id))


async def set_stage(transcript_id: int, stage: str | None) -> None:
    """Update a transcript's live ``pipeline_stage`` in its own short transaction.

    Kept independent of the pipeline's transaction so stage updates are pollable mid-run
    and survive a pipeline rollback (a failed run still ends up showing ``Greska``).
    """
    from sqlalchemy import update

    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import Transkript

    async with AsyncSessionLocal() as db:
        await db.execute(
            update(Transkript).where(Transkript.id == transcript_id).values(pipeline_stage=stage)
        )
        await db.commit()


async def import_drive_folder(folder_id: str, uploader_id, language: str | None = "bs") -> dict:
    """Public entry point. Flags the importer as running so the admin UI shows live
    state (for manual *and* scheduled runs), then delegates. The flag is always cleared,
    even on error. Returns the {queued, skipped, errors} summary."""
    from app.services.schedule.runtime_state import mark_done, mark_running

    mark_running()
    result = {"queued": 0, "skipped": 0, "errors": 0}
    try:
        result = await _import_drive_folder(folder_id, uploader_id, language)
        return result
    finally:
        mark_done(
            f"Imported {result['queued']}, skipped {result['skipped']}, "
            f"errors {result['errors']}"
        )


async def _import_drive_folder(folder_id: str, uploader_id, language: str | None = "bs") -> dict:
    """
    Import all supported files from a Google Drive folder, reusing the same path
    as the manual `/transcripts/upload` route. Idempotent: files already imported
    from this folder (matched by the ``gdrive:<folder_id>:<name>`` naziv) are
    skipped. Called as a FastAPI BackgroundTask.

    ``language`` is the ISO code used to transcribe audio (e.g. ``"bs"``); a falsy
    value lets Whisper auto-detect per file (for mixed-language folders).
    """
    from sqlalchemy import select

    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import FormatTip, Transkript, TranskStatusTip
    from app.services.storage.google_drive_service import GoogleDriveService
    from app.services.storage.storage_service import StorageService
    from app.services.transcript.file_utils import (
        MAX_FILE_SIZE,
        classify_file,
        extract_pdf_text,
    )

    drive = GoogleDriveService()
    try:
        files = drive.list_files(folder_id)
    except Exception:
        logger.exception("Failed to list Drive folder folder_id=%s", folder_id)
        return {"queued": 0, "skipped": 0, "errors": 0}

    queued = skipped = errors = 0

    async with AsyncSessionLocal() as db:
        existing = await db.execute(
            select(Transkript.id, Transkript.naziv).where(
                Transkript.naziv.like(f"gdrive:{folder_id}:%")
            )
        )
        # file name -> (transcript_id, recorded modifiedTime or None for legacy)
        recorded: dict[str, tuple[int, str | None]] = {}
        for tid, nz in existing.all():
            parsed = _parse_drive_naziv(nz, folder_id)
            if parsed:
                recorded[parsed[0]] = (tid, parsed[1])

        for f in files:
            name = f["name"]
            mtime = f.get("modifiedTime")
            naziv = _drive_naziv(folder_id, name, mtime)

            rec = recorded.get(name)
            replace_id: int | None = None
            if rec is not None:
                rec_id, rec_mtime = rec
                if rec_mtime is not None and rec_mtime == mtime:
                    skipped += 1  # already imported this exact version
                    continue
                # Changed file (newer modifiedTime) or a legacy import with no
                # recorded version — replace the old transcript. Deferred until the
                # new file is validated below so a failed re-import keeps the old one.
                replace_id = rec_id

            try:
                content = drive.download_file(f["id"])
            except Exception:
                logger.exception("Failed to download Drive file id=%s", f.get("id"))
                errors += 1
                continue

            if len(content) > MAX_FILE_SIZE:
                logger.warning("Skipping oversized Drive file %s (%d bytes)", naziv, len(content))
                skipped += 1
                continue

            is_audio, is_text, is_pdf = classify_file(f.get("mimeType", ""), f["name"])
            if not (is_audio or is_text or is_pdf):
                skipped += 1
                continue

            raw_text: str | None = None
            storage_path: str | None = None
            try:
                if is_audio:
                    safe_name = (
                        f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{f['name']}"
                    )
                    storage_path = StorageService().upload(
                        path=safe_name,
                        data=content,
                        content_type=f.get("mimeType") or "application/octet-stream",
                    )
                elif is_text:
                    raw_text = content.decode("utf-8", errors="replace")
                else:  # pdf
                    raw_text = extract_pdf_text(content)
            except Exception:
                logger.exception("Failed to prepare Drive file %s", naziv)
                errors += 1
                continue

            # New version validated — now drop the superseded import (same transaction).
            if replace_id is not None:
                await purge_transcript(db, replace_id)
                recorded.pop(name, None)

            transkript = Transkript(
                id_korisnika_upload=uploader_id,
                naziv=naziv,
                file_path=storage_path,
                format=FormatTip.audio if is_audio else FormatTip.tekst,
                raw_text=raw_text,
                jezik=language or None,
                status=TranskStatusTip.sirovi,
            )
            db.add(transkript)
            await db.commit()
            await db.refresh(transkript)
            recorded[name] = (transkript.id, mtime)
            queued += 1

            try:
                await process_transcript(transkript.id, language)
            except Exception:
                # process_transcript already logged and marked the row Odbacen;
                # keep going so one bad file doesn't abort the batch.
                errors += 1

    logger.info(
        "Drive import done folder_id=%s queued=%d skipped=%d errors=%d",
        folder_id, queued, skipped, errors,
    )
    return {"queued": queued, "skipped": skipped, "errors": errors}


async def process_transcript(transcript_id: int, language: str | None = "bs") -> None:
    """
    Download audio (if needed), transcribe via Groq Whisper, run the preprocessing
    pipeline, and persist masked segments + Q&A pairs.  Called as a FastAPI BackgroundTask.

    ``language`` is the ISO code passed to Whisper; a falsy value auto-detects.
    """
    from sqlalchemy import select

    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import FormatTip, Transkript, TranskStatusTip
    from app.services.ai.kb_indexing import embed_pending
    from app.services.preprocessing.pipeline import run_pipeline
    from app.services.storage.storage_service import StorageService
    from app.services.transcript.transcription_service import TranscriptionService

    # --- Phase A: transcription + preprocessing (one atomic commit) ---
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Transkript).where(Transkript.id == transcript_id)
        )
        transkript = result.scalar_one_or_none()
        if not transkript:
            return

        try:
            raw_text = transkript.raw_text or ""

            if transkript.format == FormatTip.audio and transkript.file_path:
                await set_stage(transcript_id, "Transkripcija")
                storage = StorageService()
                audio_bytes = storage.download(transkript.file_path)
                suffix = os.path.splitext(transkript.file_path)[1] or ".audio"
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                        tmp.write(audio_bytes)
                        tmp_path = tmp.name
                    raw_text = TranscriptionService().transcribe(tmp_path, language=language)
                finally:
                    if tmp_path and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                transkript.raw_text = raw_text

            await set_stage(transcript_id, "Ciscenje")
            pipeline_result = await run_pipeline(transcript_id, raw_text, db)
            transkript.processed_text = pipeline_result.masked_text
            transkript.status = TranskStatusTip.obradjeno
            await db.commit()

        except Exception:
            logger.exception(
                "Failed to process transcript transcript_id=%s", transcript_id
            )
            # Discard any half-built pipeline rows, then record the failure cleanly.
            await db.rollback()
            failed = (await db.execute(
                select(Transkript).where(Transkript.id == transcript_id)
            )).scalar_one_or_none()
            if failed:
                failed.status = TranskStatusTip.odbacen
                await db.commit()
            await set_stage(transcript_id, "Greska")
            raise

    # --- Phase B: resumable embed sweep (outside the pipeline transaction) ---
    await set_stage(transcript_id, "Ugradnja")
    try:
        await embed_pending()
    except Exception:
        # Sweep is resumable — leave vector_id NULL; startup self-heal will finish it.
        logger.exception("embed_pending failed after transcript_id=%s", transcript_id)
    await set_stage(transcript_id, None)
