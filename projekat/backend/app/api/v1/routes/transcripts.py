from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.db.models.transcript import Transcript, TranscriptType
from app.api.v1.deps import require_role
from app.schemas.transcript import TranscriptRead, TranscriptUploadResponse
from app.tasks.transcript_tasks import process_transcript_task

router = APIRouter(prefix="/transcripts", tags=["transcripts"])

ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a"}
ALLOWED_TEXT_TYPES = {"text/plain"}


@router.post("/upload", response_model=TranscriptUploadResponse)
async def upload_transcript(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.agent)),
):
    """
    Upload a transcript (text) or audio file.
    Triggers async Celery task for processing.
    """
    is_audio = file.content_type in ALLOWED_AUDIO_TYPES
    is_text = file.content_type in ALLOWED_TEXT_TYPES

    if not is_audio and not is_text:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    # TODO: save file to storage (filesystem / S3)
    file_path = f"uploads/{file.filename}"

    transcript = Transcript(
        uploaded_by=current_user.id,
        original_filename=file.filename,
        file_path=file_path,
        transcript_type=TranscriptType.audio if is_audio else TranscriptType.text,
    )
    db.add(transcript)
    await db.commit()
    await db.refresh(transcript)

    # Dispatch Celery task
    task = process_transcript_task.delay(str(transcript.id))
    transcript.celery_task_id = task.id
    await db.commit()

    return TranscriptUploadResponse(
        transcript_id=transcript.id,
        task_id=task.id,
        message="Upload successful. Processing started.",
    )


@router.get("/", response_model=list[TranscriptRead])
async def list_transcripts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.agent)),
):
    from sqlalchemy import select
    result = await db.execute(select(Transcript).order_by(Transcript.created_at.desc()))
    return result.scalars().all()


@router.get("/{transcript_id}", response_model=TranscriptRead)
async def get_transcript(
    transcript_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin, UserRole.agent)),
):
    from sqlalchemy import select
    result = await db.execute(select(Transcript).where(Transcript.id == transcript_id))
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return transcript
