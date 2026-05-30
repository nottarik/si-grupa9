from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.schemas.escalation import EscalationInfo


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[HistoryMessage] = []
    session_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str | None = None
    confidence_score: float = 0.0
    is_low_confidence: bool = False
    source_id: int | None = None
    source_topic: str | None = None
    interaction_id: int | None = None
    session_id: int
    escalation: Optional[EscalationInfo] = None
    is_agent_chat: bool = False
    needs_escalation: bool = False
    escalation_trigger: str | None = None


class FeedbackRequest(BaseModel):
    interaction_id: int
    is_positive: bool | None = None
    rating: float | None = None
    comment: str | None = None
    is_incorrect: bool = False


class SessionRateRequest(BaseModel):
    rating: float
    comment: str | None = None
