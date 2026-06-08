import os
from groq import Groq

from app.core.config import settings

_client: Groq | None = None

# Priming prompts bias Whisper toward the target language's spelling and diacritics.
# This markedly improves Bosnian output — without it Whisper tends to strip č/ć/ž/š/đ
# or drift toward Croatian/Serbian spelling, which is what made Bosnian imports imprecise.
_LANGUAGE_PROMPTS = {
    "bs": "Transkript poziva korisničke podrške na bosanskom jeziku. Tekst sadrži slova č, ć, ž, š i đ.",
    "de": "Transkript eines Kundendienstanrufs auf Deutsch.",
}


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

    def transcribe(self, audio_path: str, language: str | None = "en") -> str:
        client = get_groq_client()
        filename = os.path.basename(audio_path)
        # temperature=0 makes decoding deterministic, which is more accurate than the
        # default sampling for clean call-center speech.
        kwargs = {"model": settings.WHISPER_MODEL, "temperature": 0.0}
        # A falsy language lets Whisper auto-detect (used for mixed-language folders).
        if language:
            kwargs["language"] = language
            prompt = _LANGUAGE_PROMPTS.get(language)
            if prompt:
                kwargs["prompt"] = prompt
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                **kwargs,
            )
        return transcription.text if hasattr(transcription, "text") else str(transcription)
