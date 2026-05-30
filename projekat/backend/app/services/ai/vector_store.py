from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from app.core.config import settings

VECTOR_SIZE = 384  # all-MiniLM-L6-v2 output dimension


_qdrant_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        kwargs = {"url": settings.QDRANT_URL}
        if settings.QDRANT_API_KEY:
            kwargs["api_key"] = settings.QDRANT_API_KEY
        _qdrant_client = QdrantClient(**kwargs)
    return _qdrant_client


class VectorStoreService:
    """Handles all Qdrant operations: collection setup, indexing, search."""

    def __init__(self):
        self.client = get_qdrant_client()
        self.collection = settings.QDRANT_COLLECTION_NAME

    def ensure_collection(self):
        """Create collection if it doesn't exist. Call once at startup."""
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )

    def index_item(self, item_id: str, vector: list[float], payload: dict):
        """Index a single Q&A item into Qdrant."""
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=item_id, vector=vector, payload=payload)],
        )

    def search(self, query_vector: list[float], top_k: int = 5):
        """Return top-k most similar items."""
        return self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )

    def delete_item(self, item_id: str):
        from qdrant_client.models import PointIdsList
        self.client.delete(
            collection_name=self.collection,
            points_selector=PointIdsList(points=[item_id]),
        )


_vector_store_instance: VectorStoreService | None = None


def get_vector_store() -> VectorStoreService:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStoreService()
    return _vector_store_instance
