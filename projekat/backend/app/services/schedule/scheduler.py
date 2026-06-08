"""In-process scheduler for the admin-controlled Google Drive auto-import.

A single asyncio loop (started from the FastAPI lifespan) ticks once a minute, reads
the admin's schedule from ``drive_sync_schedule``, and runs the import when it's due.
This lives in the app process on purpose: the deployment runs a single always-warm
replica (Container Apps min=max=1), so there's exactly one loop and no double-firing.
No external cron, no extra dependency.
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select

from app.core.config import settings
from app.db.models.schedule import DriveSyncSchedule
from app.db.models.user import Korisnik, UlogaTip

logger = logging.getLogger(__name__)

_TICK_SECONDS = 60


def get_runtime_state() -> dict:
    """Snapshot of the importer's live state (running flag + last result), shared with
    the manual import path so the UI shows both the same way."""
    from app.services.schedule import runtime_state
    return runtime_state.snapshot()

# The admin picks times in Bosnian local time; we store/compare in UTC. ZoneInfo
# handles CET/CEST DST, so "daily at 02:00" stays 02:00 Sarajevo year-round.
BOSNIA_TZ = ZoneInfo("Europe/Sarajevo")


def compute_next_run(cfg: DriveSyncSchedule, after: datetime) -> datetime:
    """First run (as UTC) strictly after ``after`` that matches the schedule.

    ``hour``/``minute``/``day_of_week`` are interpreted in Bosnian local time; the
    arithmetic is done on wall-clock fields in that zone, then converted to UTC.
    """
    after_local = after.astimezone(BOSNIA_TZ)
    base = after_local.replace(second=0, microsecond=0)

    if cfg.frequency == "hourly":
        cand = base.replace(minute=min(cfg.minute, 59))
        if cand <= after_local:
            cand += timedelta(hours=1)
    elif cfg.frequency == "weekly":
        cand = base.replace(hour=cfg.hour, minute=cfg.minute)
        cand += timedelta(days=(cfg.day_of_week - cand.weekday()) % 7)
        if cand <= after_local:
            cand += timedelta(days=7)
    else:  # daily (default)
        cand = base.replace(hour=cfg.hour, minute=cfg.minute)
        if cand <= after_local:
            cand += timedelta(days=1)

    return cand.astimezone(timezone.utc)


async def ensure_table() -> None:
    """Create the schedule table and seed its singleton row if missing (idempotent).

    Production has no automatic Alembic step, so this guarantees the table exists on
    first boot without a manual migration. Harmless where the migration already ran.
    """
    from app.db.session import AsyncSessionLocal, engine

    async with engine.begin() as conn:
        await conn.run_sync(DriveSyncSchedule.__table__.create, checkfirst=True)
        # create_all won't add columns to a table that already exists, and production
        # has no Alembic step — add `language` defensively so an existing schedule row
        # gets the column on deploy. Idempotent via IF NOT EXISTS.
        await conn.exec_driver_sql(
            "ALTER TABLE drive_sync_schedule "
            "ADD COLUMN IF NOT EXISTS language VARCHAR NOT NULL DEFAULT 'en'"
        )

    async with AsyncSessionLocal() as db:
        exists = (
            await db.execute(select(DriveSyncSchedule.id).where(DriveSyncSchedule.id == 1))
        ).scalar_one_or_none()
        if exists is None:
            db.add(DriveSyncSchedule(id=1))
            await db.commit()


async def get_or_create_config(db) -> DriveSyncSchedule:
    cfg = (
        await db.execute(select(DriveSyncSchedule).where(DriveSyncSchedule.id == 1))
    ).scalar_one_or_none()
    if cfg is None:
        cfg = DriveSyncSchedule(id=1)
        db.add(cfg)
        await db.flush()
    return cfg


async def _tick() -> None:
    from app.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        cfg = await get_or_create_config(db)
        if not cfg.enabled:
            return

        now = datetime.now(timezone.utc)
        nxt = cfg.next_run_at
        if nxt is None:
            cfg.next_run_at = compute_next_run(cfg, now)
            await db.commit()
            return
        if nxt.tzinfo is None:  # some drivers return naive UTC
            nxt = nxt.replace(tzinfo=timezone.utc)
        if now < nxt:
            return

        # Due — advance the schedule first so a slow import can't re-trigger itself.
        folder_id = settings.GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID
        configured = bool(settings.GOOGLE_SERVICE_ACCOUNT_JSON and folder_id)
        uploader_id = None
        if configured:
            uploader_id = (
                await db.execute(
                    select(Korisnik.id).where(Korisnik.uloga == UlogaTip.administrator).limit(1)
                )
            ).scalar_one_or_none()

        # "auto" → None so Whisper detects the language per file (mixed-language folders).
        language = None if cfg.language == "auto" else cfg.language

        cfg.last_run_at = now
        cfg.next_run_at = compute_next_run(cfg, now)
        await db.commit()

    if not configured:
        logger.warning("Drive schedule is enabled but Drive import is not configured — skipping run.")
        return
    if uploader_id is None:
        logger.warning("Drive schedule due but no administrator user to attribute the import to.")
        return

    from app.tasks.transcript_tasks import import_drive_folder

    logger.info("Scheduled Drive import starting (folder=%s)", folder_id)
    try:
        # import_drive_folder manages the running flag + last_result itself, so a manual
        # run surfaces the same live state in the UI as a scheduled one.
        await import_drive_folder(folder_id, uploader_id, language)
    except Exception:
        logger.exception("Scheduled Drive import failed")


async def scheduler_loop() -> None:
    await ensure_table()
    logger.info("Drive sync scheduler started (tick aligned to minute boundary)")
    while True:
        try:
            await _tick()
        except Exception:
            logger.exception("Drive sync scheduler tick failed")
        # Sleep to the top of the next minute (not a flat 60s) so a run scheduled for
        # HH:MM fires at HH:MM:00 instead of up to a minute late, depending on when the
        # loop happened to start. compute_next_run already targets second 0.
        now = datetime.now(timezone.utc)
        await asyncio.sleep(_TICK_SECONDS - (now.second + now.microsecond / 1_000_000))
