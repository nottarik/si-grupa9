import os
from groq import Groq

from app.core.config import settings

_client: Groq | None = None


def get_groq_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


class TranscriptionService:
    """
    Transcribes audio files via Groq's Whisper API.
    Returns a plain text transcript.
    """

    def transcribe(self, audio_path: str, language: str = "bs") -> str:
        client = get_groq_client()
        filename = os.path.basename(audio_path)
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                model=settings.WHISPER_MODEL,
                language=language,
                response_format="text",
            )
        return transcription if isinstance(transcription, str) else str(transcription)
