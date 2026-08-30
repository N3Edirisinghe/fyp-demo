"""
Session 3 — same visit as Session 2

- Plain, memoryless, text-only chatbot using the SAME LLM as Session 2
- This is the H3 control/baseline arm — isolates the effect of the
  proposed architecture from the base LLM itself (Section 5.3)
"""

import streamlit as st

from src.conditions.baseline import run_baseline_turn
from src.memory.db import log_survey_response
from src.utils.validators import is_valid_participant_id

st.title("Session 3 — Standard Assistant Chat")

participant_id = st.text_input("Participant ID (e.g. P01)")
if participant_id and not is_valid_participant_id(participant_id):
    st.error("Please enter a valid anonymized participant ID.")
    st.stop()

st.divider()

if "session3_history" not in st.session_state:
    st.session_state.session3_history = []

user_text = st.text_input("Type your message")

if user_text and participant_id and st.button("Send"):
    response = run_baseline_turn(participant_id=participant_id, session=3, user_text=user_text)
    st.session_state.session3_history.append(("You", user_text))
    st.session_state.session3_history.append(("Assistant", response))

for speaker, message in st.session_state.session3_history:
    st.write(f"**{speaker}:** {message}")

st.divider()
st.subheader("End-of-session survey (H3 baseline)")
st.caption("Rate each statement from 1 (strongly disagree) to 5 (strongly agree).")

H3_ITEMS = [
    "Overall, I am satisfied with this interaction.",
    "This assistant felt more helpful than a typical AI assistant.",
]

if participant_id:
    with st.form("h3_baseline_survey"):
        responses = [st.slider(item, 1, 5, 3) for item in H3_ITEMS]
        submitted = st.form_submit_button("Submit survey")
        if submitted:
            for item, response in zip(H3_ITEMS, responses, strict=False):
                log_survey_response(participant_id, 3, "H3", "baseline", item, response)
            st.success("Survey submitted. Thank you for participating in this study!")
