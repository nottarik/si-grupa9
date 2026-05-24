import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1.router import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    from app.services.ai.vector_store import get_vector_store
    try:
        get_vector_store().ensure_collection()
    except Exception as exc:
        logging.getLogger("app.startup").warning(
            "Qdrant unreachable at startup — will retry on first request. %s", exc
        )
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
