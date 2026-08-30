"""
Speech-to-text via Groq's hosted Whisper endpoint (free tier).

Kept as a thin wrapper so the ASR provider can be swapped (e.g. for a
self-hosted faster-whisper model) without touching calling code.
"""

from groq import Groq

from config.settings import settings

_client = Groq(api_key=settings.groq_api_key)


def transcribe_audio(audio_file_path: str, language: str | None = None) -> str:
    """
    Transcribe an audio file to text.

    Args:
        audio_file_path: path to a WAV/MP3 file captured from the user.
        language: optional ISO 639-1 code (e.g. "en") to hint the ASR model.

    Returns:
        The transcribed text (empty string on failure — callers should
        handle this gracefully rather than crash a live study session).
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = _client.audio.transcriptions.create(
                file=(audio_file_path, audio_file.read()),
                model="whisper-large-v3",
                language=language,
                response_format="text",
            )
        return str(response).strip()
    except Exception as exc:  # noqa: BLE001 — log and degrade gracefully
        print(f"[ASR] Transcription failed: {exc}")
        return ""
