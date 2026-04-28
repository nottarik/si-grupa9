"""
Periodic privacy cleanup: nullify raw_text for transcripts older than 24 h.
"""
import asyncio
from datetime import datetime, timedelta, timezone

from app.workers.celery_app import celery_app


@celery_app.task(name="app.tasks.cleanup_tasks.cleanup_raw_transcripts")
def cleanup_raw_transcripts() -> None:
    asyncio.run(_do_cleanup())


async def _do_cleanup() -> None:
    from sqlalchemy import select
    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import Transkript

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Transkript).where(
                Transkript.datum_uploada < cutoff,
                Transkript.raw_text.isnot(None),
            )
        )
        stale = result.scalars().all()
        for t in stale:
            t.raw_text = None
        if stale:
            await db.commit()
