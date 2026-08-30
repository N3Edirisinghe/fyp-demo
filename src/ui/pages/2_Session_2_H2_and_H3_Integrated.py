"""
Session 2 — Week 2 (approx. 1 week after Session 1)

- Memory is ON: the companion retrieves and references Session 1's
  conversation and detected emotions (Section 5.2)
- This is the H2 "memory-enabled" (post) condition and the H3 "integrated
  system" arm
- Ends with the H2-post survey and the H3 satisfaction survey
"""

import streamlit as st

from src.conditions.memory_enabled import run_integrated_turn
from src.memory.db import log_survey_response
from src.memory.profiling import build_emotional_profile
from src.utils.validators import is_valid_participant_id

st.title("Session 2 — The Companion Remembers You")

participant_id = st.text_input("Participant ID (e.g. P01)")
if participant_id and not is_valid_participant_id(participant_id):
    st.error("Please enter a valid anonymized participant ID.")
    st.stop()

if participant_id:
    with st.expander("Your emotional profile so far (from Session 1)"):
        st.json(build_emotional_profile(participant_id))

st.divider()
st.subheader("Speak to the companion")

audio_file = st.audio_input("Record your message")

if audio_file is not None and participant_id:
    audio_path = f"data/processed/session2_{participant_id}.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file.getvalue())

    transcript = st.text_input("Transcript (auto-filled by ASR in production)")

    if transcript and st.button("Submit turn"):
        result = run_integrated_turn(
            participant_id=participant_id,
            session=2,
            audio_path=audio_path,
            transcript=transcript,
            use_memory=True,  # Session 2 = memory ON (H2-post, H3-integrated)
        )
        st.success("Recorded.")
        st.write(f"**Companion:** {result['response_text']}")
        if result["retrieved_memories"]:
            with st.expander("Memories the companion recalled"):
                for memory in result["retrieved_memories"]:
                    st.write(f"- \"{memory['text']}\" (felt {memory['emotion']})")

st.divider()
st.subheader("End-of-session survey")
st.caption("Rate each statement from 1 (strongly disagree) to 5 (strongly agree).")

H2_ITEMS = [
    "The companion felt personalized to me.",
    "I trust the companion's responses.",
    "I felt a sense of companionship during this session.",
]
H3_ITEMS = [
    "Overall, I am satisfied with this interaction.",
    "This companion felt more helpful than a typical AI assistant.",
]

if participant_id:
    with st.form("h2_h3_survey"):
        st.markdown("**Personalization, Trust & Companionship (H2)**")
        h2_responses = [st.slider(item, 1, 5, 3, key=f"h2_{i}") for i, item in enumerate(H2_ITEMS)]
        st.markdown("**Overall Satisfaction (H3)**")
        h3_responses = [st.slider(item, 1, 5, 3, key=f"h3_{i}") for i, item in enumerate(H3_ITEMS)]

        submitted = st.form_submit_button("Submit survey")
        if submitted:
            for item, response in zip(H2_ITEMS, h2_responses, strict=False):
                log_survey_response(participant_id, 2, "H2", "post", item, response)
            for item, response in zip(H3_ITEMS, h3_responses, strict=False):
                log_survey_response(participant_id, 2, "H3", "integrated", item, response)
            st.success("Survey submitted. Please continue to Session 3.")
