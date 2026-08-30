"""
Session 1 — Week 1

- Collects voice input, runs BOTH voice and text emotion classifiers (H1)
- Immediately asks the participant to self-report their actual emotion,
  which becomes the ground-truth label for H1 accuracy/F1 scoring
- Memory is OFF this session — these interactions double as the H2
  "memory-disabled" (pre) baseline per the pre/post design
- Ends with the H2-baseline half of the trust/personalization/companionship survey
"""

import streamlit as st

from config.settings import settings
from src.conditions.memory_enabled import run_integrated_turn
from src.memory.db import log_survey_response
from src.utils.validators import is_valid_participant_id

st.title("Session 1 — Voice Interaction & Emotion Check")

participant_id = st.text_input("Participant ID (e.g. P01)")
if participant_id and not is_valid_participant_id(participant_id):
    st.error("Please enter a valid anonymized participant ID (issued by the research team).")
    st.stop()

st.divider()
st.subheader("Step 1 — Speak to the companion")

audio_file = st.audio_input("Record your message")

if audio_file is not None and participant_id:
    audio_path = f"data/processed/session1_{participant_id}.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file.getvalue())

    # NOTE: transcript would normally come from src/asr/speech_to_text.py
    # Left as a manual field here for local testing without an API key.
    transcript = st.text_input("Transcript (auto-filled by ASR in production)")

    if transcript:
        st.subheader("Step 2 — How did you actually feel when you said that?")
        self_label = st.selectbox(
            "This is used as ground truth to score the emotion classifiers (H1).",
            settings.emotion_labels,
        )

        if st.button("Submit turn"):
            result = run_integrated_turn(
                participant_id=participant_id,
                session=1,
                audio_path=audio_path,
                transcript=transcript,
                self_reported_emotion=self_label,
                use_memory=False,  # Session 1 = memory OFF (H1 + H2 baseline)
            )
            st.success("Recorded.")
            st.write(f"**Companion:** {result['response_text']}")
            with st.expander("Debug: detected emotions (H1 comparison)"):
                st.json(
                    {
                        "voice_emotion": result["voice_emotion"],
                        "text_emotion": result["text_emotion"],
                        "agreement": result["emotion_agreement"],
                        "self_reported": self_label,
                    }
                )

st.divider()
st.subheader("Step 3 — End-of-session survey (H2 baseline)")
st.caption("Rate each statement from 1 (strongly disagree) to 5 (strongly agree).")

H2_ITEMS = [
    "The companion felt personalized to me.",
    "I trust the companion's responses.",
    "I felt a sense of companionship during this session.",
]

if participant_id:
    with st.form("h2_baseline_survey"):
        responses = [st.slider(item, 1, 5, 3) for item in H2_ITEMS]
        submitted = st.form_submit_button("Submit survey")
        if submitted:
            for item, response in zip(H2_ITEMS, responses, strict=False):
                log_survey_response(
                    participant_id=participant_id,
                    session=1,
                    hypothesis="H2",
                    scale_name="baseline",
                    item=item,
                    response=response,
                )
            st.success("Survey submitted. Thank you — see you in Session 2 next week.")
