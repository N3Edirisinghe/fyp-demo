"""
Generates the companion's response text, conditioned on detected emotion
and (when the condition calls for it) retrieved memory + emotional profile
(Section 5.3). Supports both providers named in the proposal's resource
requirements: Groq and Gemini.
"""

from config.settings import settings

SYSTEM_PROMPT_INTEGRATED = """You are an emotionally supportive AI companion taking part in a
research study. Respond warmly and naturally to the user, taking into account their detected
emotional state and any relevant memory context provided. Keep responses concise (2-4 sentences).
You are not a therapist and must not present yourself as a substitute for professional mental
health care."""

SYSTEM_PROMPT_BASELINE = """You are a helpful AI assistant taking part in a research study.
Respond naturally to the user. Keep responses concise (2-4 sentences)."""


def _build_prompt(
    user_text: str,
    emotion_label: str | None = None,
    memory_context: list[dict] | None = None,
) -> str:
    parts = []
    if emotion_label:
        parts.append(f"[Detected user emotion: {emotion_label}]")
    if memory_context:
        memory_lines = "\n".join(f"- {m['text']} (felt {m['emotion']})" for m in memory_context)
        parts.append(f"[Relevant past context:\n{memory_lines}]")
    parts.append(f"User: {user_text}")
    return "\n".join(parts)


def generate_response(
    user_text: str,
    condition: str,
    emotion_label: str | None = None,
    memory_context: list[dict] | None = None,
) -> str:
    """
    Args:
        user_text: the user's transcribed utterance.
        condition: 'baseline' (H3 control — memoryless, no emotion input)
                   or 'memory_enabled' (H2/H3 integrated condition).
        emotion_label: detected emotion, only used when condition != 'baseline'.
        memory_context: retrieved memories, only used when condition == 'memory_enabled'.
    """
    if condition == "baseline":
        system_prompt = SYSTEM_PROMPT_BASELINE
        prompt = f"User: {user_text}"
    else:
        system_prompt = SYSTEM_PROMPT_INTEGRATED
        prompt = _build_prompt(user_text, emotion_label, memory_context)

    if settings.llm_provider == "groq":
        return _call_groq(system_prompt, prompt)
    return _call_gemini(system_prompt, prompt)


def _call_groq(system_prompt: str, prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=settings.groq_api_key)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return completion.choices[0].message.content.strip()


def _call_gemini(system_prompt: str, prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt)
    response = model.generate_content(prompt)
    return response.text.strip()
