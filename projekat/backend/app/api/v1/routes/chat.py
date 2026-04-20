from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import User
from app.api.v1.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest
from app.services.ai.rag_service import RagService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Main chatbot endpoint. Receives a user question,
    runs RAG pipeline, returns answer with confidence score.
    """
    rag = RagService(db)
    result = await rag.answer(question=payload.question, user_id=current_user.id)
    return result


@router.post("/feedback")
async def submit_feedback(
    payload: FeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit feedback (thumbs up/down, rating, or report incorrect answer)
    for a given chat interaction.
    """
    from app.db.models.knowledge import Feedback
    feedback = Feedback(
        interaction_id=payload.interaction_id,
        user_id=current_user.id,
        is_positive=payload.is_positive,
        rating=payload.rating,
        comment=payload.comment,
        is_incorrect=payload.is_incorrect,
    )
    db.add(feedback)
    await db.commit()
    return {"message": "Feedback saved"}
