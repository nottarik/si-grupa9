from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.session import Base


class QAStatus(str, enum.Enum):
    pending_approval = "pending_approval"
    active = "active"
    rejected = "rejected"
    archived = "archived"


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transcript_id = Column(UUID(as_uuid=True), ForeignKey("transcripts.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    status = Column(Enum(QAStatus), default=QAStatus.pending_approval)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    qdrant_point_id = Column(String, nullable=True)  # ID u vektorskoj bazi
    version = Column(String, default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ChatInteraction(Base):
    __tablename__ = "chat_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=True)
    source_item_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_items.id"), nullable=True)
    is_low_confidence = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interaction_id = Column(UUID(as_uuid=True), ForeignKey("chat_interactions.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    rating = Column(Float, nullable=True)  # 1-5
    is_positive = Column(Boolean, nullable=True)  # thumbs up/down
    comment = Column(Text, nullable=True)
    is_incorrect = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
