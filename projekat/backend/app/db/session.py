from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

_connect_args: dict = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # File-bazirani SQLite (testovi): TestClient pokreće app u zasebnom threadu
    # dok test helperi commit-uju iz drugog event loopa → "database is locked".
    # check_same_thread=False dopušta dijeljenje konekcije; timeout tjera pisca
    # da čeka na lock umjesto da odmah pukne.
    _connect_args = {"check_same_thread": False, "timeout": 30}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    connect_args=_connect_args,
)

if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, _):
        # WAL dopušta istovremene čitaoce uz jednog pisca; busy_timeout čeka lock.
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA busy_timeout=30000")
        cur.close()

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
