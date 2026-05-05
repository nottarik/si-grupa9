from pydantic import BaseModel, field_validator
from datetime import date, datetime

from app.db.models.transcript import TranskStatusTip, FormatTip


class TranscriptRead(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    celery_task_id: str | None
    datum_uploada: datetime | None

    model_config = {"from_attributes": True}


class TranscriptDetail(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    celery_task_id: str | None
    datum_uploada: datetime | None
    processed_text: str | None

    model_config = {"from_attributes": True}


class TranscriptUploadResponse(BaseModel):
    transcript_id: int
    task_id: str | None
    message: str


class TranscriptManualCreate(BaseModel):
    date: date
    content: str
    agent_name: str

    @field_validator("content")
    @classmethod
    def content_min_length(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 20:
            raise ValueError("Transcript content must be at least 20 characters long")
        return stripped

    @field_validator("agent_name")
    @classmethod
    def agent_name_required(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Agent name is required")
        return stripped


class TranscriptManualResponse(BaseModel):
    transcript_id: int
    message: str


class TranscriptUpdate(BaseModel):
    naziv: str | None = None
    processed_text: str | None = None
