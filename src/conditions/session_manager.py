"""
Orchestrates which condition a participant experiences at each study
session, matching the design agreed in docs/research_proposal_mapping.md:

  Session 1 (Week 1): voice + live self-labeling, memory OFF
                       -> H1 ground-truth collection, H2 baseline (pre)
  Session 2 (Week 2): same participant, memory ON, system recalls Session 1
                       -> H2 (post) + H3 integrated arm
  Session 3 (Week 2): plain memoryless text-only chatbot, same LLM
                       -> H3 baseline arm

Kept deliberately simple (a lookup table) so the experimental design is
easy to audit against the proposal during supervisor review.
"""

from enum import Enum


class StudySession(int, Enum):
    SESSION_1 = 1
    SESSION_2 = 2
    SESSION_3 = 3


SESSION_CONFIG = {
    StudySession.SESSION_1: {
        "condition": "no_memory",
        "use_memory": False,
        "collect_self_label": True,  # ground truth for H1
        "surveys": ["H2_baseline"],
    },
    StudySession.SESSION_2: {
        "condition": "memory_enabled",
        "use_memory": True,
        "collect_self_label": False,
        "surveys": ["H2_post", "H3_integrated"],
    },
    StudySession.SESSION_3: {
        "condition": "baseline",
        "use_memory": False,
        "collect_self_label": False,
        "surveys": ["H3_baseline"],
    },
}


def get_session_config(session: StudySession) -> dict:
    return SESSION_CONFIG[session]
