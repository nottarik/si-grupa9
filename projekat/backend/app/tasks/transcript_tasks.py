import asyncio
from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_transcript_task(self, transcript_id: str):
    try:
        asyncio.run(_process(transcript_id))
    except Exception as exc:
        raise self.retry(exc=exc)


async def _process(transcript_id: str):
    from sqlalchemy import select
    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import Transkript, FormatTip
    from app.db.models.knowledge import UnosBazeZnanja
    from app.services.pipeline.pipeline_service import PipelineService
    from app.services.transcript.transcription_service import TranscriptionService

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Transkript).where(Transkript.id == transcript_id))
        transkript = result.scalar_one_or_none()
        if not transkript:
            return

        try:
            raw_text = transkript.raw_text or ""

            if transkript.format == FormatTip.audio and transkript.file_path:
                svc = TranscriptionService()
                raw_text = svc.transcribe(transkript.file_path)
                transkript.raw_text = raw_text

            pipeline = PipelineService()
            result_data = pipeline.process(raw_text)

            transkript.processed_text = result_data.masked_text

            for pair in result_data.qa_pairs:
                item = UnosBazeZnanja(
                    pitanje=pair["question"],
                    odgovor=pair["answer"],
                    status_aprovacije="NaCekanju",
                )
                db.add(item)

            transkript.status = "Obradjeno"

        except Exception:
            transkript.status = "Odbacen"
            raise

        finally:
            await db.commit()
