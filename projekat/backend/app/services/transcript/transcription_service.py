from faster_whisper import WhisperModel
from app.core.config import settings

_model: WhisperModel | None = None


def get_whisper_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel(
            settings.WHISPER_MODEL_SIZE,
            device=settings.WHISPER_DEVICE,
            compute_type="int8",
        )
    return _model


class TranscriptionService:
    """
    Transcribes audio files locally using faster-whisper.
    Returns a plain text transcript with speaker turns where possible.
    """

    def transcribe(self, audio_path: str, language: str = "bs") -> str:
        model = get_whisper_model()
        segments, info = model.transcribe(audio_path, language=language)
        lines = [segment.text.strip() for segment in segments]
        return "\n".join(lines)
