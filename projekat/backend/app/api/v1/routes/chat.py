from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.api.v1.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest
from app.services.ai.rag_service import RagService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    rag = RagService(db)
    result = await rag.answer(question=payload.question, user_id=current_user.id)
    return result


@router.post("/feedback")
async def submit_feedback(
    payload: FeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    from app.db.models.knowledge import Feedback

    ocjena: float | None = payload.rating
    if ocjena is None and payload.is_positive is not None:
        ocjena = 5.0 if payload.is_positive else 1.0

    komentar = payload.comment or ""
    if payload.is_incorrect:
        komentar = f"[Netačan odgovor] {komentar}".strip()

    feedback = Feedback(
        id_odgovora=payload.interaction_id,
        id_korisnika=current_user.id,
        ocjena=ocjena,
        komentar=komentar or None,
        tip="KorisnikOcjena",
    )
    db.add(feedback)
    await db.commit()
    return {"message": "Feedback saved"}
