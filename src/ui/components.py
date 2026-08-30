"""Small reusable Streamlit UI helpers shared across session pages."""

import streamlit as st


def likert_scale(label: str, key: str) -> int:
    """Renders a standard 1-5 Likert item and returns the selected value."""
    return st.slider(label, min_value=1, max_value=5, value=3, key=key)


def consent_banner() -> bool:
    """Shows the informed-consent reminder; returns True once acknowledged."""
    st.info(
        "By continuing, you confirm you have read and agreed to the informed consent "
        "form provided by the research team, and understand you may withdraw at any time."
    )
    return st.checkbox("I consent to continue.")
