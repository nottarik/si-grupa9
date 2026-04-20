from sentence_transformers import SentenceTransformer
from app.core.config import settings

# Loaded once at module level – reused across requests
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


class EmbeddingService:
    """Converts text to dense vectors using a local sentence-transformers model."""

    def embed(self, text: str) -> list[float]:
        model = get_model()
        vector = model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        model = get_model()
        vectors = model.encode(texts, normalize_embeddings=True, batch_size=32)
        return vectors.tolist()
