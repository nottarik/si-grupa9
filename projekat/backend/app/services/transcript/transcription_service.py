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

    def transcribe(self, audio_path: str, language: str | None = "bs") -> str:
        client = get_groq_client()
        filename = os.path.basename(audio_path)
        kwargs = {"model": settings.WHISPER_MODEL}
        # A falsy language lets Whisper auto-detect (used for mixed-language folders).
        if language:
            kwargs["language"] = language
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                **kwargs,
            )
        return transcription.text if hasattr(transcription, "text") else str(transcription)
