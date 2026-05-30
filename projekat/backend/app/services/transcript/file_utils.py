"""Shared helpers for classifying and extracting transcript source files.

Used by both the manual upload route (`routes/transcripts.py`) and the
Google Drive batch import task (`tasks/transcript_tasks.py`) so the two paths
stay in lockstep.
"""
import io

from fastapi import HTTPException

ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a", "audio/ogg"}
ALLOWED_TEXT_TYPES = {"text/plain", "text/x-plain"}
ALLOWED_PDF_TYPES = {"application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def classify_file(content_type: str, filename: str) -> tuple[bool, bool, bool]:
    """Return (is_audio, is_text, is_pdf), falling back to the file extension."""
    ct = content_type.lower()
    is_audio = ct in ALLOWED_AUDIO_TYPES
    is_text = ct in ALLOWED_TEXT_TYPES
    is_pdf = ct in ALLOWED_PDF_TYPES

    if not (is_audio or is_text or is_pdf):
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext == "pdf":
            is_pdf = True
        elif ext == "txt":
            is_text = True
        elif ext in {"mp3", "wav", "m4a", "ogg"}:
            is_audio = True

    return is_audio, is_text, is_pdf


def extract_pdf_text(content: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not extract text from PDF: {exc}")
