"""
Text-to-speech via Edge-TTS (free, no API key required).

Supports basic tone/rate adjustment so the companion's delivery can be
modulated based on the selected response strategy (Section 7.5 of the
long-term product vision) — optional for the core H1/H2/H3 study, but
kept here since the proposal's response pipeline benefits from it.
"""

import asyncio
import uuid

import edge_tts

DEFAULT_VOICE = "en-US-JennyNeural"


async def _synthesize(text: str, voice: str, rate: str, output_path: str) -> None:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(output_path)


def synthesize_speech(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    output_dir: str = "data/processed/tts_output",
) -> str:
    """
    Convert text to a speech audio file.

    Args:
        text: the response text to speak.
        voice: an Edge-TTS voice name.
        rate: speech rate adjustment, e.g. "-10%" for a slower, gentler tone.
        output_dir: directory to write the generated audio file to.

    Returns:
        Path to the generated .mp3 file.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.mp3")
    asyncio.run(_synthesize(text, voice, rate, output_path))
    return output_path
