from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.db.session import Base


class DriveSyncSchedule(Base):
    """Admin-controlled schedule for the automatic Google Drive import.

    Single-row config (id == 1). The in-process scheduler reads this every tick and
    runs the import when ``next_run_at`` is due. ``frequency`` is one of
    ``hourly`` / ``daily`` / ``weekly``; ``hour``/``minute``/``day_of_week`` are UTC.
    """

    __tablename__ = "drive_sync_schedule"

    id = Column(Integer, primary_key=True)  # singleton row, always 1
    enabled = Column(Boolean, nullable=False, default=False)
    frequency = Column(String, nullable=False, default="daily")  # hourly | daily | weekly
    hour = Column(Integer, nullable=False, default=2)             # 0–23 UTC (daily/weekly)
    minute = Column(Integer, nullable=False, default=0)           # 0–59
    day_of_week = Column(Integer, nullable=False, default=0)      # Mon=0 … Sun=6 (weekly)
    # ISO language code for transcription (en | bs | de) or "auto" to let Whisper detect.
    language = Column(String, nullable=False, default="en", server_default="en")
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
