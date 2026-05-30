import logging
import threading
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from app.core.config import settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None
_model_lock = threading.Lock()


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


@lru_cache(maxsize=512)
def _embed_cached(text: str) -> tuple[float, ...]:
    """Module-level cached embed — same text always produces the same vector."""
    with _model_lock:
        vector = get_model().encode(text, normalize_embeddings=True)
    return tuple(vector.tolist())


class EmbeddingService:
    """Converts text to dense vectors using a local sentence-transformers model."""

    def embed(self, text: str) -> list[float]:
        info = _embed_cached.cache_info()
        result = list(_embed_cached(text))
        new_info = _embed_cached.cache_info()
        if new_info.hits > info.hits:
            logger.debug("EMBED cache hit (hits=%d misses=%d)", new_info.hits, new_info.misses)
        else:
            logger.debug("EMBED cache miss (hits=%d misses=%d)", new_info.hits, new_info.misses)
        return result

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        with _model_lock:
            vectors = get_model().encode(texts, normalize_embeddings=True, batch_size=32)
        return vectors.tolist()


_embedding_instance: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = EmbeddingService()
    return _embedding_instance
