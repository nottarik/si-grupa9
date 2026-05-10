import logging
import os
import tempfile

logger = logging.getLogger(__name__)


async def process_transcript(transcript_id: int) -> None:
    """
    Download audio (if needed), transcribe via Groq Whisper, run the preprocessing
    pipeline, and persist masked segments + Q&A pairs.  Called as a FastAPI BackgroundTask.
    """
    from sqlalchemy import select

    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import FormatTip, Transkript, TranskStatusTip
    from app.services.preprocessing.pipeline import run_pipeline
    from app.services.storage.storage_service import StorageService
    from app.services.transcript.transcription_service import TranscriptionService

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
                storage = StorageService()
                audio_bytes = storage.download(transkript.file_path)
                suffix = os.path.splitext(transkript.file_path)[1] or ".audio"
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                        tmp.write(audio_bytes)
                        tmp_path = tmp.name
                    raw_text = TranscriptionService().transcribe(tmp_path)
                finally:
                    if tmp_path and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                transkript.raw_text = raw_text

            pipeline_result = await run_pipeline(transcript_id, raw_text, db)
            transkript.processed_text = pipeline_result.masked_text
            transkript.status = TranskStatusTip.obradjeno

        except Exception:
            logger.exception(
                "Failed to process transcript transcript_id=%s", transcript_id
            )
            transkript.status = TranskStatusTip.odbacen
            raise

        finally:
            await db.commit()
