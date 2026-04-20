import asyncio
from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_transcript_task(self, transcript_id: str):
    """
    Celery task that:
      1. Loads transcript from DB
      2. Runs Speech-to-Text if audio
      3. Runs Processing Pipeline (normalize, mask PII, extract Q&A)
      4. Saves extracted Q&A pairs to DB with status pending_approval
      5. Updates transcript status to 'processed'
    """
    try:
        asyncio.run(_process(transcript_id))
    except Exception as exc:
        raise self.retry(exc=exc)


async def _process(transcript_id: str):
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import Transcript, TranscriptStatus, TranscriptType
    from app.db.models.knowledge import KnowledgeItem, QAStatus
    from app.services.pipeline.pipeline_service import PipelineService
    from app.services.transcript.transcription_service import TranscriptionService
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Transcript).where(Transcript.id == transcript_id))
        transcript = result.scalar_one_or_none()
        if not transcript:
            return

        transcript.status = TranscriptStatus.processing
        await db.commit()

        try:
            raw_text = transcript.raw_text or ""

            # Step 1: transcribe audio if needed
            if transcript.transcript_type == TranscriptType.audio and transcript.file_path:
                svc = TranscriptionService()
                raw_text = svc.transcribe(transcript.file_path)
                transcript.raw_text = raw_text

            # Step 2: run pipeline
            pipeline = PipelineService()
            result_data = pipeline.process(raw_text)

            transcript.processed_text = result_data.masked_text

            # Step 3: save Q&A pairs for admin review
            for pair in result_data.qa_pairs:
                item = KnowledgeItem(
                    transcript_id=transcript.id,
                    question=pair["question"],
                    answer=pair["answer"],
                    status=QAStatus.pending_approval,
                )
                db.add(item)

            transcript.status = TranscriptStatus.processed

        except Exception:
            transcript.status = TranscriptStatus.failed
            raise

        finally:
            await db.commit()
