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

        vector = await asyncio.to_thread(EmbeddingService().embed, item.pitanje)
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


@router.post("/reindex", summary="Re-embed all approved items with question-only vectors")
async def reindex_all(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    from app.services.ai.embedding_service import EmbeddingService
    from app.services.ai.vector_store import VectorStoreService

    result = await db.execute(
        select(UnosBazeZnanja).where(UnosBazeZnanja.status_aprovacije == "Odobren")
    )
    items = result.scalars().all()
    ok, failed = 0, 0
    for item in items:
        try:
            vector = await asyncio.to_thread(EmbeddingService().embed, item.pitanje)
            vector_id = item.vector_id or str(uuid.uuid4())
            await asyncio.to_thread(
                VectorStoreService().index_item,
                vector_id,
                vector,
                {"item_id": item.id, "question": item.pitanje, "answer": item.odgovor},
            )
            item.vector_id = vector_id
            ok += 1
        except Exception as exc:
            logger.warning("Reindex failed for item %s: %s", item.id, exc)
            failed += 1
    await db.commit()
    return {"reindexed": ok, "failed": failed}


@router.get("/debug")
async def debug_qdrant(
    q: str = "test",
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    from app.services.ai.embedding_service import EmbeddingService
    from app.services.ai.vector_store import VectorStoreService

    vs = VectorStoreService()
    try:
        info = vs.client.get_collection(vs.collection)
        collection_info = {
            "name": vs.collection,
            "points_count": info.points_count,
            "vectors_size": info.config.params.vectors.size if info.config.params.vectors else None,
            "distance": str(info.config.params.vectors.distance) if info.config.params.vectors else None,
        }
    except Exception as exc:
        collection_info = {"error": str(exc)}

    try:
        vector = await asyncio.to_thread(EmbeddingService().embed, q)
        hits = await asyncio.to_thread(vs.search, vector, 5)
        search_results = [
            {"score": round(h.score, 4), "payload": h.payload}
            for h in hits
        ]
    except Exception as exc:
        search_results = {"error": str(exc)}

    approved_count = (await db.execute(
        select(UnosBazeZnanja).where(UnosBazeZnanja.status_aprovacije == "Odobren")
    )).scalars().all()
    with_vectors = [i for i in approved_count if i.vector_id]

    return {
        "collection": collection_info,
        "query": q,
        "search_results": search_results,
        "db_approved_items": len(approved_count),
        "db_items_with_vector_id": len(with_vectors),
    }


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
