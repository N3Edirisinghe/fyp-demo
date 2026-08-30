"""
Tests for the LLM response generator's prompt construction logic (does not
call the real Groq/Gemini API — that requires a live key and network access
and is exercised manually/in staging instead).
"""

from src.llm.response_generator import _build_prompt


def test_build_prompt_includes_emotion_and_memory():
    prompt = _build_prompt(
        user_text="I'm feeling okay today",
        emotion_label="neutral",
        memory_context=[{"text": "I was stressed about exams", "emotion": "fear"}],
    )

    assert "neutral" in prompt
    assert "stressed about exams" in prompt
    assert "I'm feeling okay today" in prompt


def test_build_prompt_without_memory():
    prompt = _build_prompt(user_text="Hello", emotion_label="happy", memory_context=None)

    assert "happy" in prompt
    assert "Relevant past context" not in prompt
