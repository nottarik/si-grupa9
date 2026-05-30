"""Shared embed + index helpers for knowledge-base entries.

Centralizes the "embed a question and upsert it into Qdrant" logic that used to be
copy-pasted across the knowledge routes, and adds a crash-safe resumable sweep used
by the pipeline and the startup self-heal.

Vector ids are **deterministic** (``uuid5`` of the DB row id) so re-indexing the same
item upserts the same Qdrant point instead of creating a duplicate — making the sweep
idempotent even if the process dies between the Qdrant write and the ``vector_id`` commit.
"""

import asyncio
import logging
import uuid

from sqlalchemy import select

from app.db.models.knowledge import UnosBazeZnanja
from app.services.ai.embedding_service import get_embedding_service
from app.services.ai.vector_store import get_vector_store

logger = logging.getLogger(__name__)

# Fixed namespace so kb_vector_id is stable across processes/restarts.
_KB_NAMESPACE = uuid.UUID("8f1d2e7a-4c3b-5a6d-9e0f-1a2b3c4d5e6f")

# Bound peak memory during the sweep (model.encode also mini-batches internally).
_SWEEP_CHUNK = 50


def kb_vector_id(item_id: int) -> str:
    """Deterministic Qdrant point id for a knowledge-base row."""
    return str(uuid.uuid5(_KB_NAMESPACE, str(item_id)))


async def embed_and_index_item(item: UnosBazeZnanja) -> None:
    """Embed one item's question and upsert it into Qdrant, setting ``item.vector_id``.

    The caller owns the DB commit and any error handling. Raises on embed/index failure.
    """
    vector = await asyncio.to_thread(get_embedding_service().embed, item.pitanje)
    vid = kb_vector_id(item.id)
    await asyncio.to_thread(
        get_vector_store().index_item,
        vid,
        vector,
        {"item_id": item.id, "question": item.pitanje, "answer": item.odgovor},
    )
    item.vector_id = vid


async def embed_pending() -> int:
    """Embed + index every approved KB entry that has no vector yet.

    Resumable and idempotent: a row is durable in the DB (``Odobren``, ``vector_id IS NULL``)
    before it ever reaches Qdrant, so a crash mid-sweep leaves only un-embedded rows that the
    next call finishes — never an orphan vector. Commits per chunk so progress survives a kill.

    Returns the number of items embedded.
    """
    from app.db.session import AsyncSessionLocal

    embedded = 0
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(UnosBazeZnanja).where(
                UnosBazeZnanja.status_aprovacije == "Odobren",
                UnosBazeZnanja.aktivan == True,  # noqa: E712
                UnosBazeZnanja.vector_id.is_(None),
            )
        )
        items = result.scalars().all()
        if not items:
            return 0

        vs = get_vector_store()
        for start in range(0, len(items), _SWEEP_CHUNK):
            chunk = items[start : start + _SWEEP_CHUNK]
            vectors = await asyncio.to_thread(
                get_embedding_service().embed_batch, [i.pitanje for i in chunk]
            )
            for item, vector in zip(chunk, vectors):
                try:
                    await asyncio.to_thread(
                        vs.index_item,
                        kb_vector_id(item.id),
                        vector,
                        {"item_id": item.id, "question": item.pitanje, "answer": item.odgovor},
                    )
                    item.vector_id = kb_vector_id(item.id)
                    embedded += 1
                except Exception:
                    logger.warning("embed_pending: indexing failed for item %s", item.id)
            await db.commit()  # persist this chunk's vector_ids before the next

    if embedded:
        logger.info("embed_pending: embedded %d pending KB item(s)", embedded)
    return embedded
