"""
H2/H3 experimental condition: full integrated pipeline — voice + text
emotion detection, memory retrieval, emotional profiling, and emotionally
calibrated response generation (Sections 5.1-5.3).
"""

from src.emotion.fusion import EmotionComparisonPipeline
from src.llm.response_generator import generate_response
from src.memory.db import log_interaction
from src.memory.vector_store import retrieve_relevant_memories, store_memory

_emotion_pipeline = EmotionComparisonPipeline()


def run_integrated_turn(
    participant_id: str,
    session: int,
    audio_path: str,
    transcript: str,
    self_reported_emotion: str | None = None,
    use_memory: bool = True,
) -> dict:
    """
    Runs one full conversational turn for the integrated condition.

    Args:
        use_memory: set False to run Session 1 (H1 data collection, no
            memory yet — this doubles as the H2 "memory-disabled" baseline
            per the pre/post design described in docs/research_proposal_mapping.md).

    Returns:
        dict with the assistant's response text and the detected emotions,
        for display in the Streamlit UI and for logging.
    """
    h1_result = _emotion_pipeline.analyze(audio_path, transcript)

    memory_context = []
    if use_memory:
        memory_context = retrieve_relevant_memories(participant_id, transcript)

    response_text = generate_response(
        user_text=transcript,
        condition="memory_enabled" if use_memory else "no_memory",
        emotion_label=h1_result.voice_label,
        memory_context=memory_context,
    )

    embedding_id = None
    if use_memory:
        embedding_id = store_memory(
            participant_id=participant_id,
            session=session,
            text=transcript,
            emotion_label=h1_result.voice_label,
        )

    log_interaction(
        participant_id=participant_id,
        session=session,
        condition="memory_enabled" if use_memory else "no_memory",
        transcript=transcript,
        voice_emotion_label=h1_result.voice_label,
        voice_emotion_confidence=h1_result.voice_confidence,
        text_emotion_label=h1_result.text_label,
        text_emotion_confidence=h1_result.text_confidence,
        self_reported_emotion=self_reported_emotion,
        embedding_id=embedding_id,
    )

    return {
        "response_text": response_text,
        "voice_emotion": h1_result.voice_label,
        "text_emotion": h1_result.text_label,
        "emotion_agreement": h1_result.agreement,
        "retrieved_memories": memory_context,
    }
