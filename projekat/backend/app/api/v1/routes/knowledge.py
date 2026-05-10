import asyncio
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.knowledge import UnosBazeZnanja
from app.api.v1.deps import require_role

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
logger = logging.getLogger(__name__)


@router.get("/pending", response_model=list[dict])
async def list_pending(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(
        select(UnosBazeZnanja).where(UnosBazeZnanja.status_aprovacije == "NaCekanju")
    )
    items = result.scalars().all()
    return [
        {
            "id": i.id,
            "question": i.pitanje,
            "answer": i.odgovor,
            "category": i.id_kategorije,
            "status": i.status_aprovacije,
        }
        for i in items
    ]


@router.post("/{item_id}/approve")
async def approve_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(UnosBazeZnanja).where(UnosBazeZnanja.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status_aprovacije = "Odobren"
    item.aktivan = True

    # Embed and index into Qdrant now that the item is approved.
    # Done here (one item at a time) rather than during upload to avoid OOM.
    try:
        from app.services.ai.embedding_service import EmbeddingService
        from app.services.ai.vector_store import VectorStoreService

        text = f"{item.pitanje} {item.odgovor}"
        vector = await asyncio.to_thread(EmbeddingService().embed, text)
        vector_id = str(uuid.uuid4())

        await asyncio.to_thread(
            VectorStoreService().index_item,
            vector_id,
            vector,
            {"item_id": item.id, "question": item.pitanje, "answer": item.odgovor},
        )
        item.vector_id = vector_id
    except Exception:
        logger.warning("Qdrant indexing failed for item %s; approved without vector.", item_id)

    await db.commit()
    return {"message": "Item approved"}


@router.post("/{item_id}/reject")
async def reject_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(UnosBazeZnanja).where(UnosBazeZnanja.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status_aprovacije = "Odbijen"
    item.aktivan = False
    await db.commit()
    return {"message": "Item rejected"}
