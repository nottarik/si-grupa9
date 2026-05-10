import hashlib
import logging

logger = logging.getLogger(__name__)


def safe_log(event: str, *, transcript_id: int, **counts: int | float) -> None:
    """Log a pipeline audit event. Only accepts numeric values — never raw text."""
    extra = " ".join(f"{k}={v}" for k, v in counts.items())
    logger.info("pipeline.%s transcript_id=%s %s", event, transcript_id, extra)


def text_hash(text: str) -> str:
    """SHA-256 prefix safe to include in error logs instead of raw text."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]
