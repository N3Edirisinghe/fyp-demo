"""
Admin/researcher dashboard — monitor data collection progress and export
anonymized data for statistical analysis (paired t-test / Wilcoxon, per
Section 5.5). Not intended for participant access; add a password gate
before deploying publicly (see docs/deployment_guide.md).
"""

import pandas as pd
import streamlit as st

from src.memory.db import _get_connection

st.title("Admin Dashboard")

password = st.text_input("Access code", type="password")
if password != st.secrets.get("ADMIN_PASSWORD", "changeme"):
    st.warning("Enter the researcher access code to continue.")
    st.stop()

conn = _get_connection()

st.subheader("Interactions")
interactions_df = pd.read_sql_query("SELECT * FROM interactions ORDER BY timestamp DESC", conn)
st.dataframe(interactions_df)
st.download_button(
    "Download interactions.csv",
    interactions_df.to_csv(index=False),
    file_name="interactions.csv",
)

st.subheader("Survey Responses")
survey_df = pd.read_sql_query("SELECT * FROM survey_responses ORDER BY timestamp DESC", conn)
st.dataframe(survey_df)
st.download_button(
    "Download survey_responses.csv",
    survey_df.to_csv(index=False),
    file_name="survey_responses.csv",
)

st.subheader("H1 Progress: Self-Labeled Interactions Collected")
h1_progress = interactions_df[interactions_df["self_reported_emotion"].notna()]
st.metric("Ground-truth-labeled utterances", len(h1_progress))

st.subheader("Participants per Session")
st.bar_chart(interactions_df.groupby("session")["participant_id"].nunique())
