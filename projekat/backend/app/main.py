import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1.router import api_router

logger = logging.getLogger(__name__)


async def _startup_self_heal():
    """Resume anything an earlier process left half-done (no durable queue exists).

    (a) finish any approved KB items that were never embedded, and (b) re-run transcripts
    left stuck in Sirovi (their in-process BackgroundTask died with the server). Runs in the
    background so it never blocks startup.
    """
    from datetime import datetime, timedelta, timezone

    from sqlalchemy import select

    from app.db.session import AsyncSessionLocal
    from app.db.models.transcript import Transkript, TranskStatusTip
    from app.services.ai.kb_indexing import embed_pending
    from app.tasks.transcript_tasks import process_transcript

    log = logging.getLogger("app.startup")
    try:
        # No race: finishing un-embedded approved items is always safe.
        await embed_pending()
        # Only re-queue Sirovi rows old enough that their (now-dead) BackgroundTask
        # can't still be running — avoids double-processing a fresh upload at startup.
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=1)
        async with AsyncSessionLocal() as db:
            ids = (await db.execute(
                select(Transkript.id).where(
                    Transkript.status == TranskStatusTip.sirovi,
                    Transkript.datum_uploada < cutoff,
                )
            )).scalars().all()
        for tid in ids:
            try:
                await process_transcript(tid)
            except Exception:
                log.exception("self-heal: re-processing transcript %s failed", tid)
        if ids:
            log.info("self-heal: re-queued %d stuck transcript(s)", len(ids))
    except Exception:
        log.exception("startup self-heal failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    import logging
    from app.services.ai.vector_store import get_vector_store
    try:
        get_vector_store().ensure_collection()
    except Exception as exc:
        logging.getLogger("app.startup").warning(
            "Qdrant unreachable at startup — will retry on first request. %s", exc
        )
    # Keep a reference so the background task isn't garbage-collected mid-run.
    app.state.heal_task = asyncio.create_task(_startup_self_heal())
    yield


app = FastAPI(
    title="Call Centar Chatbot API",
    description="RAG-based chatbot trained on call center transcripts",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "env": settings.APP_ENV}


@app.get("/heartbeat", tags=["health"])
async def heartbeat():
    """Lightweight liveness probe for Uptime Robot — no DB queries."""
    return {"ok": True}
