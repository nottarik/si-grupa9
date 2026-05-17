from pydantic import BaseModel


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[HistoryMessage] = []


class ChatResponse(BaseModel):
    answer: str
    confidence_score: float
    is_low_confidence: bool
    source_id: int | None = None
    interaction_id: int


class FeedbackRequest(BaseModel):
    interaction_id: int
    is_positive: bool | None = None
    rating: float | None = None
    comment: str | None = None
    is_incorrect: bool = False
