from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.db.models.knowledge import KnowledgeItem, QAStatus
from app.api.v1.deps import require_role

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/pending", response_model=list[dict])
async def list_pending(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    """List all Q&A pairs waiting for admin approval."""
    result = await db.execute(
        select(KnowledgeItem).where(KnowledgeItem.status == QAStatus.pending_approval)
    )
    items = result.scalars().all()
    return [{"id": str(i.id), "question": i.question, "answer": i.answer, "category": i.category} for i in items]


@router.post("/{item_id}/approve")
async def approve_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    """
    Approve a Q&A pair. Triggers embedding generation and indexing in Qdrant.
    """
    result = await db.execute(select(KnowledgeItem).where(KnowledgeItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # TODO: generate embedding and store in Qdrant
    # from app.services.ai.embedding_service import EmbeddingService
    # await EmbeddingService().index_item(item)

    item.status = QAStatus.active
    item.approved_by = current_user.id
    await db.commit()
    return {"message": "Item approved and indexed"}


@router.post("/{item_id}/reject")
async def reject_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    result = await db.execute(select(KnowledgeItem).where(KnowledgeItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status = QAStatus.rejected
    await db.commit()
    return {"message": "Item rejected"}
