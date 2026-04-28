import asyncio
from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_transcript_task(self, transcript_id: int):
    try:
        asyncio.run(_process(int(transcript_id)))
    except Exception as exc:
        raise self.retry(exc=exc)


async def _process(transcript_id: int):
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from app.core.config import settings
    from app.db.session import Base  # noqa: F401 — ensures metadata is populated
    from app.db.models.user import Korisnik  # noqa: F401 — registers korisnik in metadata
    from app.db.models.transcript import Transkript, FormatTip
    from app.db.models.knowledge import UnosBazeZnanja
    from app.services.pipeline.pipeline_service import PipelineService
    from app.services.transcript.transcription_service import TranscriptionService

    # Create a fresh engine per task invocation so it binds to the current
    # event loop (asyncio.run() creates a new loop each call; a module-level
    # engine keeps stale loop references and raises "Future attached to a
    # different loop" on the second execution).
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with SessionLocal() as db:
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
    finally:
        await engine.dispose()
