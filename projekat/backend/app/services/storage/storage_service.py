from supabase import create_client, Client

from app.core.config import settings

_client: Client | None = None


def get_supabase_client() -> Client:
    global _client
    if _client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY must be configured."
            )
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client


class StorageService:
    """Wrapper around Supabase Storage for transcript file uploads."""

    def __init__(self):
        self.bucket = settings.SUPABASE_BUCKET

    def upload(self, path: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        client = get_supabase_client()
        client.storage.from_(self.bucket).upload(
            path=path,
            file=data,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return path

    def download(self, path: str) -> bytes:
        client = get_supabase_client()
        return client.storage.from_(self.bucket).download(path)

    def delete(self, path: str) -> None:
        client = get_supabase_client()
        client.storage.from_(self.bucket).remove([path])
