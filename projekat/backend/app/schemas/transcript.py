import re

from pydantic import BaseModel, field_validator
from datetime import date, datetime

from app.db.models.transcript import TranskStatusTip, FormatTip


def _display_naziv(v: str) -> str:
    """Drive imports are stored as ``gdrive:<folder_id>:<filename>`` (with the Drive
    modifiedTime appended after ``::v::`` for change detection) for folder-scoped
    dedup; show only the original filename to the user."""
    if v.startswith("gdrive:"):
        parts = v.split(":", 2)
        if len(parts) == 3:
            return parts[2].split("::v::", 1)[0]
    return v


def _check_transcript_format(text: str) -> None:
    lines = text.splitlines()
    has_agent = any(
        re.match(r"^\s*AGENT\s*:", line, re.IGNORECASE) and line.split(":", 1)[-1].strip()
        for line in lines
    )
    has_user = any(
        re.match(r"^\s*(USER|KORISNIK)\s*:", line, re.IGNORECASE) and line.split(":", 1)[-1].strip()
        for line in lines
    )
    if not has_agent:
        raise ValueError("Transcript must contain at least one line in format 'AGENT: text'")
    if not has_user:
        raise ValueError("Transcript must contain at least one line in format 'USER: text'")


class TranscriptRead(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    pipeline_stage: str | None = None
    celery_task_id: str | None
    datum_uploada: datetime | None

    model_config = {"from_attributes": True}

    @field_validator("naziv")
    @classmethod
    def clean_naziv(cls, v: str) -> str:
        return _display_naziv(v)


class TranscriptDetail(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    celery_task_id: str | None
    datum_uploada: datetime | None
    processed_text: str | None

    model_config = {"from_attributes": True}

    @field_validator("naziv")
    @classmethod
    def clean_naziv(cls, v: str) -> str:
        return _display_naziv(v)


class TranscriptUploadResponse(BaseModel):
    transcript_id: int
    task_id: str | None
    message: str


class TranscriptManualCreate(BaseModel):
    date: date
    content: str
    agent_name: str

    @field_validator("content")
    @classmethod
    def content_valid(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 20:
            raise ValueError("Transcript content must have at least 20 characters")
        _check_transcript_format(stripped)
        return stripped

    @field_validator("agent_name")
    @classmethod
    def agent_name_required(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Agent name is required")
        return stripped


class TranscriptManualResponse(BaseModel):
    transcript_id: int
    message: str


class TranscriptUpdate(BaseModel):
    naziv: str | None = None
    processed_text: str | None = None


class TranscribePreviewResponse(BaseModel):
    text: str
    quality_warning: str | None
    filename: str


class DriveImportRequest(BaseModel):
    # Optional: when omitted, the route falls back to the configured default folder
    # (the one-click "Run complete pipeline" button sends no folder).
    folder_id: str | None = None
    # ISO code for audio transcription; "auto" lets Whisper detect per file.
    language: str = "bs"

    @field_validator("folder_id")
    @classmethod
    def folder_id_clean(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip() or None


class DriveFileStatus(BaseModel):
    name: str
    status: str  # "queued" (new, being imported) | "skipped" (already imported)


class DriveImportResponse(BaseModel):
    folder_id: str
    message: str
    files: list[DriveFileStatus] = []


class AudioTranscriptConfirm(BaseModel):
    text: str
    agent_name: str
    date: date
    filename: str
    language: str = "bs"

    @field_validator("text")
    @classmethod
    def text_required(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 20:
            raise ValueError("Transcript content must have at least 20 characters")
        return stripped
