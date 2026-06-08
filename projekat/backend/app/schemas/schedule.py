from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Frequency = Literal["hourly", "daily", "weekly"]
Language = Literal["en", "bs", "de", "auto"]


class DriveFileProgress(BaseModel):
    name: str
    # pending | importing | imported | skipped | failed
    status: str


class DriveScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    enabled: bool
    frequency: Frequency
    hour: int
    minute: int
    day_of_week: int
    language: Language = "en"
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    # Live runner state (not persisted) — lets the UI show a run in progress.
    running: bool = False
    cancelling: bool = False
    last_result: Optional[str] = None
    files: list[DriveFileProgress] = []


class DriveScheduleUpdate(BaseModel):
    enabled: bool
    frequency: Frequency
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)
    day_of_week: int = Field(ge=0, le=6)
    language: Language = "en"
