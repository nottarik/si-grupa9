from pydantic import BaseModel
from uuid import UUID


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    confidence_score: float
    is_low_confidence: bool
    source_id: UUID | None = None
    interaction_id: UUID


class FeedbackRequest(BaseModel):
    interaction_id: UUID
    is_positive: bool | None = None
    rating: float | None = None
    comment: str | None = None
    is_incorrect: bool = False
