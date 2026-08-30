"""
H3 control condition: a conventional, memoryless, text-only AI assistant
using the SAME underlying LLM as the integrated system, so that any
measured difference in satisfaction is attributable to the proposed
architecture (voice emotion + memory) rather than to a stronger base model
(Section 5.3).
"""

from src.llm.response_generator import generate_response
from src.memory.db import log_interaction


def run_baseline_turn(participant_id: str, session: int, user_text: str) -> str:
    """No ASR emotion path, no memory retrieval — pure text in, text out."""
    response = generate_response(user_text=user_text, condition="baseline")

    log_interaction(
        participant_id=participant_id,
        session=session,
        condition="baseline",
        transcript=user_text,
    )
    return response
