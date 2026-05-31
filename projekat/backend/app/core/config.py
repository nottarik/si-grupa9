from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://chatbot:chatbot_pass@localhost:5432/chatbot_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "knowledge_base"
    QDRANT_API_KEY: str = ""

    # AI
    GROQ_API_KEY: str = ""
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    WHISPER_MODEL: str = "whisper-large-v3"
    RAG_TOP_K: int = 5
    RAG_CONFIDENCE_THRESHOLD: float = 0.55
    RAG_CONFIDENCE_THRESHOLD_LOW: float = 0.35
    # A question the classifier flags off-topic only overrides that verdict and answers
    # from the KB above this (stricter) floor — keeps the agent from wandering off topic
    # on weak coincidental matches, while a real KB entry (near-exact) still answers.
    RAG_OFFTOPIC_THRESHOLD: float = 0.5

    # Google Drive batch import (service account JSON key as a single string)
    GOOGLE_SERVICE_ACCOUNT_JSON: str = ""
    # Default folder the one-click "Run complete pipeline" button scans when no
    # folder is supplied in the request.
    GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID: str = ""

    # Supabase Storage
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_BUCKET: str = "transcripts"

    # PII token map encryption (Fernet key, base64url-encoded 32 bytes).
    # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    # If empty, an ephemeral key is generated at startup (dev only — maps won't survive restarts).
    TOKEN_MAP_KEY: str = ""

    # Internal API (used by GitHub Actions cron to hit /internal/* endpoints)
    INTERNAL_API_KEY: str = ""

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    @property
    def allowed_origins_list(self) -> list[str]:
        v = self.ALLOWED_ORIGINS.strip()
        if v.startswith("["):
            import json
            return json.loads(v)
        return [item.strip() for item in v.split(",") if item.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
