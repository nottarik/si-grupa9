from fastapi import APIRouter
from app.api.v1.routes import auth, chat, internal, knowledge, transcripts, users

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(transcripts.router)
api_router.include_router(knowledge.router)
api_router.include_router(internal.router)
api_router.include_router(users.router)
