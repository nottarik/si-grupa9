from pydantic import BaseModel
from uuid import UUID
from app.db.models.transcript import TranscriptStatus, TranscriptType


class TranscriptRead(BaseModel):
    id: UUID
    original_filename: str
    transcript_type: TranscriptType
    status: TranscriptStatus
    celery_task_id: str | None

    model_config = {"from_attributes": True}


class TranscriptUploadResponse(BaseModel):
    transcript_id: UUID
    task_id: str
    message: str
