from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.session import Base


class TranscriptStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    processed = "processed"
    failed = "failed"


class TranscriptType(str, enum.Enum):
    text = "text"
    audio = "audio"


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    transcript_type = Column(Enum(TranscriptType), nullable=False)
    raw_text = Column(Text, nullable=True)
    processed_text = Column(Text, nullable=True)
    status = Column(Enum(TranscriptStatus), default=TranscriptStatus.pending)
    celery_task_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
