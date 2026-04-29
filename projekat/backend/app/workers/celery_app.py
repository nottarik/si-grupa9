from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "chatbot_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.transcript_tasks", "app.tasks.cleanup_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Sarajevo",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
)

# Periodic task: clear raw transcript text after 24 h (privacy requirement).
# Run Celery Beat alongside the worker to activate this schedule:
#   celery -A app.workers.celery_app beat --loglevel=info
celery_app.conf.beat_schedule = {
    "cleanup-raw-transcripts-hourly": {
        "task": "app.tasks.cleanup_tasks.cleanup_raw_transcripts",
        "schedule": 3600.0,  # every hour
    },
}
