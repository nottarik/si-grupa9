from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.transcript import Transkript, TranskStatusTip
from app.core.config import settings

router = APIRouter(prefix="/internal", tags=["internal"])

# Transcripts stuck in Sirovi for longer than this are re-queued.
_STUCK_AFTER = timedelta(minutes=5)

# Raw text older than this is nullified (privacy cleanup).
_RAW_TEXT_TTL = timedelta(hours=24)


def _require_internal_key(x_internal_key: str = Header(...)):
    if not settings.INTERNAL_API_KEY or x_internal_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid internal API key")


@router.post("/reconcile-transcripts")
async def reconcile_transcripts(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(_require_internal_key),
):
    """Re-queue any transcript stuck in Sirovi for more than 5 minutes."""
    from app.tasks.transcript_tasks import process_transcript

    cutoff = datetime.now(timezone.utc) - _STUCK_AFTER
    result = await db.execute(
        select(Transkript).where(
            Transkript.status == TranskStatusTip.sirovi,
            Transkript.datum_uploada < cutoff,
        )
    )
    stuck = result.scalars().all()
    for t in stuck:
        background_tasks.add_task(process_transcript, t.id)
    return {"requeued": len(stuck)}


@router.post("/sync-drive")
async def sync_drive(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(_require_internal_key),
):
    """Scheduled Google Drive sync: import the configured folder, same path as the
    admin one-click button. Meant to be hit on a cron by an internal-key caller.
    Idempotent — files already imported (by modifiedTime) are skipped by the task."""
    from app.db.models.user import Korisnik, UlogaTip
    from app.tasks.transcript_tasks import import_drive_folder

    if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise HTTPException(status_code=503, detail="Google Drive import is not configured.")

    folder_id = settings.GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID
    if not folder_id:
        raise HTTPException(status_code=400, detail="GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID is not set.")

    # No logged-in user on a cron run — attribute the import to an administrator so the
    # not-null id_korisnika_upload FK is satisfied (same column the upload route fills).
    uploader_id = (
        await db.execute(
            select(Korisnik.id).where(Korisnik.uloga == UlogaTip.administrator).limit(1)
        )
    ).scalar_one_or_none()
    if uploader_id is None:
        raise HTTPException(status_code=500, detail="No administrator user to attribute the import to.")

    background_tasks.add_task(import_drive_folder, folder_id, uploader_id)
    return {"started": True, "folder_id": folder_id}


@router.post("/cleanup-raw-text")
async def cleanup_raw_text(
    db: AsyncSession = Depends(get_db),
    _: str = Depends(_require_internal_key),
):
    """Nullify raw_text for transcripts older than 24 h (privacy requirement)."""
    cutoff = datetime.now(timezone.utc) - _RAW_TEXT_TTL
    result = await db.execute(
        update(Transkript)
        .where(
            Transkript.datum_uploada < cutoff,
            Transkript.raw_text.isnot(None),
        )
        .values(raw_text=None)
    )
    await db.commit()
    return {"cleaned": result.rowcount}
