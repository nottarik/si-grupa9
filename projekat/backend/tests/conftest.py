import asyncio
import os

# Postavi testnu bazu PRIJE nego se bilo šta importuje iz app-a
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-za-testove")
os.environ.setdefault("GROQ_API_KEY", "test-key")
os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-key")
os.environ.setdefault("INTERNAL_API_KEY", "test-internal-key")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")

import pytest


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Kreira sve tabele i seed-a admin korisnika."""
    import app.db.models.user       # noqa: F401
    import app.db.models.transcript # noqa: F401
    import app.db.models.knowledge  # noqa: F401

    from app.db.session import engine, AsyncSessionLocal, Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        from app.db.models.user import Korisnik, UlogaTip
        from app.core.security import get_password_hash

        existing = await db.execute(
            select(Korisnik).where(Korisnik.email == "admin@test.com")
        )
        if not existing.scalar_one_or_none():
            db.add(Korisnik(
                ime="Admin",
                prezime="Test",
                email="admin@test.com",
                hashed_password=get_password_hash("admin123"),
                uloga=UlogaTip.administrator,
                aktivan=True,
            ))
            await db.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()