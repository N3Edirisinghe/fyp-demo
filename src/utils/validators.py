"""Small input validation helpers used across the Streamlit pages."""

from config.settings import settings


def is_valid_participant_id(participant_id: str) -> bool:
    """Participant IDs should be pre-issued anonymized codes (e.g. 'P01'),
    never real names, per the ethics/consent protocol."""
    return bool(participant_id) and participant_id.strip().upper().startswith("P")


def is_valid_emotion_label(label: str) -> bool:
    return label in settings.emotion_labels


def is_valid_likert_response(value: int) -> bool:
    return isinstance(value, int) and 1 <= value <= 5
