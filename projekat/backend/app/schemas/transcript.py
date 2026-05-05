import re

from pydantic import BaseModel, field_validator
from datetime import date, datetime

from app.db.models.transcript import TranskStatusTip, FormatTip


def _check_transcript_format(text: str) -> None:
    lines = text.splitlines()
    has_agent = any(
        re.match(r"^\s*AGENT\s*:", line, re.IGNORECASE) and line.split(":", 1)[-1].strip()
        for line in lines
    )
    has_korisnik = any(
        re.match(r"^\s*KORISNIK\s*:", line, re.IGNORECASE) and line.split(":", 1)[-1].strip()
        for line in lines
    )
    if not has_agent:
        raise ValueError("Transkript mora sadržavati najmanje jednu liniju u formatu 'AGENT: tekst'")
    if not has_korisnik:
        raise ValueError("Transkript mora sadržavati najmanje jednu liniju u formatu 'KORISNIK: tekst'")


class TranscriptRead(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    celery_task_id: str | None
    datum_uploada: datetime | None

    model_config = {"from_attributes": True}


class TranscriptDetail(BaseModel):
    id: int
    naziv: str
    format: FormatTip
    status: TranskStatusTip
    celery_task_id: str | None
    datum_uploada: datetime | None
    processed_text: str | None

    model_config = {"from_attributes": True}


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
            raise ValueError("Sadržaj transkripta mora imati najmanje 20 znakova")
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
