from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.models.user import Korisnik, UlogaTip
from app.db.session import get_db
from app.schemas.schedule import DriveFileProgress, DriveScheduleRead, DriveScheduleUpdate
from app.services.schedule.scheduler import (
    compute_next_run,
    get_or_create_config,
    get_runtime_state,
)

router = APIRouter(prefix="/schedule", tags=["schedule"])


def _with_runtime(cfg) -> DriveScheduleRead:
    data = DriveScheduleRead.model_validate(cfg)
    state = get_runtime_state()
    data.running = state["running"]
    data.cancelling = state.get("cancelling", False)
    data.last_result = state.get("last_result")
    data.files = [DriveFileProgress(**f) for f in state.get("files", [])]
    return data


@router.get("/drive", response_model=DriveScheduleRead)
async def get_drive_schedule(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    return _with_runtime(await get_or_create_config(db))


@router.put("/drive", response_model=DriveScheduleRead)
async def update_drive_schedule(
    body: DriveScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    cfg = await get_or_create_config(db)
    cfg.enabled = body.enabled
    cfg.frequency = body.frequency
    cfg.hour = body.hour
    cfg.minute = body.minute
    cfg.day_of_week = body.day_of_week
    # Recompute the next run from the new settings; clear it when disabled.
    cfg.next_run_at = compute_next_run(cfg, datetime.now(timezone.utc)) if body.enabled else None
    await db.commit()
    await db.refresh(cfg)
    return _with_runtime(cfg)


@router.post("/drive/cancel", response_model=DriveScheduleRead)
async def cancel_drive_import(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    """Request the in-progress Drive import (manual or scheduled) to stop after the
    current file. No-op if nothing is running."""
    from app.services.schedule.runtime_state import request_cancel

    request_cancel()
    return _with_runtime(await get_or_create_config(db))
