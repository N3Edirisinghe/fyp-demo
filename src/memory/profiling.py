"""
Aggregates a participant's stored interaction history into an interpretable
emotional profile — dominant emotions, trend direction, recurring patterns
(Section 5.2). This is what makes the memory "explainable" rather than a
raw, unstructured log.
"""

from collections import Counter

from src.memory.db import get_participant_history


def build_emotional_profile(participant_id: str) -> dict:
    history = get_participant_history(participant_id)

    if not history:
        return {"dominant_emotion": None, "trend": "insufficient_data", "total_interactions": 0}

    emotion_sequence = [
        row["voice_emotion_label"] for row in history if row.get("voice_emotion_label")
    ]
    counts = Counter(emotion_sequence)
    dominant_emotion = counts.most_common(1)[0][0] if counts else None

    trend = _estimate_trend(emotion_sequence)

    return {
        "dominant_emotion": dominant_emotion,
        "emotion_distribution": dict(counts),
        "trend": trend,
        "total_interactions": len(history),
    }


def _estimate_trend(emotion_sequence: list[str]) -> str:
    """
    Very simple heuristic trend indicator comparing the first half of a
    participant's history to the second half. Intended for the profile
    summary shown back to the user, not as a clinical measure.
    """
    negative = {"sad", "angry", "fear"}
    if len(emotion_sequence) < 4:
        return "insufficient_data"

    midpoint = len(emotion_sequence) // 2
    first_half_negative_ratio = (
        sum(1 for e in emotion_sequence[:midpoint] if e in negative) / midpoint
    )
    second_half_negative_ratio = sum(1 for e in emotion_sequence[midpoint:] if e in negative) / (
        len(emotion_sequence) - midpoint
    )

    if second_half_negative_ratio > first_half_negative_ratio + 0.15:
        return "increasingly_negative"
    if second_half_negative_ratio < first_half_negative_ratio - 0.15:
        return "improving"
    return "stable"
