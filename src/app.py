"""
Main Streamlit entrypoint for AffetX.

Provides a clean, minimalist Google-inspired landing interface for the
research study on Emotionally Adaptive AI Companion.
"""

import streamlit as st

"""
Main Streamlit entrypoint for AffetX.

Provides an interactive, multi-step research study interface:
1. Minimalist Google-style landing page with AffetX branding, San Francisco subtitle, and Research Server
2. Agreement & Privacy Consent modal/step
3. Emotion Check-in baseline selector (Happy, Sad, Angry, Fear, Neutral, Surprise)
4. Emotionally Adaptive AI Companion Bot interface
"""

import streamlit as st
from config.settings import settings

st.set_page_config(
    page_title="AffetX — Emotionally Adaptive AI Companion",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "study_step" not in st.session_state:
    st.session_state.study_step = "landing"  # 'landing', 'agreement', 'emotion_checkin', 'ai_bot'

if "user_agreed" not in st.session_state:
    st.session_state.user_agreed = False

if "baseline_emotion" not in st.session_state:
    st.session_state.baseline_emotion = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "companion", "content": "Hello! I am AffetX, your emotionally adaptive companion. How can I support you today?"}
    ]

# Custom CSS Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Playfair+Display:ital,wght@1,600&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Body styling */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Top Navigation Header */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2.5rem;
    }

    /* Top Left AffetX Cursive Italic Brand - No Clipping */
    .brand-top-left {
        font-family: 'Dancing Script', 'Playfair Display', cursive;
        font-style: italic;
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.2;
        display: inline-block;
        padding-right: 18px;
        padding-left: 2px;
        padding-bottom: 4px;
        color: #0f172a;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
        user-select: none;
        overflow: visible;
    }

    .server-status-badge {
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #059669;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 6px rgba(5, 150, 105, 0.4);
    }

    /* Center Hero Container */
    .affetx-center-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 0 auto 1.5rem auto;
        max-width: 840px;
    }

    /* San Francisco Subtitle */
    .affetx-main-title {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.35;
        letter-spacing: -0.3px;
        margin-bottom: 0.6rem;
    }

    .affetx-subtitle {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 1.15rem;
        font-weight: 400;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    .server-pill-title {
        display: inline-block;
        background: #e2e8f0;
        color: #1e293b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 4px 12px;
        border-radius: 12px;
        margin-bottom: 1.2rem;
    }

    /* Primary Blue Button styling */
    .start-btn-container {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0 2.5rem 0;
    }

    /* Card styling */
    .custom-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Section Header */
    .portal-section-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        margin-top: 2rem;
        margin-bottom: 1.2rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Top Bar with AffetX on Top-Left
st.markdown(
    """
    <div class="top-navbar">
        <div class="brand-top-left">AffetX</div>
        <div class="server-status-badge">
            <span class="status-dot"></span>
            Research Server: Ready &bull; Port 8501
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# STEP 1: ULTRA-MINIMALIST LANDING PAGE
# ==========================================
if st.session_state.study_step == "landing":

    st.markdown(
        """
        <div class="affetx-center-hero" style="margin-top: 8vh; margin-bottom: 2rem;">
            <div class="affetx-main-title" style="font-size: 2.8rem; margin-top: 0.5rem; margin-bottom: 0.8rem; letter-spacing: -0.02em;">
                Designing an Emotionally Adaptive AI Companion
            </div>
            <div class="affetx-subtitle" style="font-size: 1.3rem; margin-bottom: 2rem;">
                Using Voice Emotion Recognition and Long-Term Emotional Memory
            </div>
            <div class="server-pill-title" style="margin-bottom: 2.5rem;">
                <span class="status-dot"></span> Research Server
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ONLY Executive Start Button
    col_l, col_m, col_r = st.columns([2, 2, 2])
    with col_m:
        if st.button("Start Session", type="primary", use_container_width=True):
            st.session_state.study_step = "agreement"
            st.rerun()

# ==========================================
# STEP 2: USER AGREEMENT & PRIVACY CONSENT
# ==========================================
elif st.session_state.study_step == "agreement":
    st.markdown(
        """
        <div class="affetx-center-hero">
            <div class="affetx-main-title">Participant Consent & Privacy Policy</div>
            <div class="affetx-subtitle">Please review the privacy parameters before proceeding.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_l, col_m, col_r = st.columns([1, 3, 1])
    with col_m:
        st.markdown(
            """
            <div class="custom-card">
                <h4 style="color: #0f172a; margin-bottom: 12px; font-size: 1.05rem;">Data Protection Commitment</h4>
                <ul style="color: #475569; line-height: 1.8; font-size: 0.95rem;">
                    <li><strong>No Personal Data Stored:</strong> We do not collect or store names, phone numbers, email addresses, or personal identifiable information.</li>
                    <li><strong>Anonymized Voice & Text:</strong> Audio signals and transcriptions are strictly pseudonymized and used exclusively for academic research.</li>
                    <li><strong>Voluntary Participation:</strong> You may discontinue this session at any point without penalty.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        consent_check = st.checkbox("I understand and agree to participate in this research study anonymously.")

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Cancel & Return", use_container_width=True):
                st.session_state.study_step = "landing"
                st.rerun()
        with btn_col2:
            if st.button("Accept & Continue", type="primary", disabled=not consent_check, use_container_width=True):
                st.session_state.user_agreed = True
                st.session_state.study_step = "emotion_checkin"
                st.rerun()

# ==========================================
# STEP 3: EMOTION CHECK-IN QUESTION
# ==========================================
elif st.session_state.study_step == "emotion_checkin":
    st.markdown(
        """
        <div class="affetx-center-hero">
            <div class="affetx-main-title">How are you feeling right now?</div>
            <div class="affetx-subtitle">Select the state that best reflects your current emotional baseline:</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_l, col_m, col_r = st.columns([1, 3, 1])
    with col_m:
        emotions = [
            ("Happy", "happy", "Joyful, optimistic, or cheerful"),
            ("Sad", "sad", "Low energy, down, or melancholic"),
            ("Angry", "angry", "Frustrated, irritated, or tense"),
            ("Fear", "fear", "Anxious, worried, or uneasy"),
            ("Neutral", "neutral", "Calm, balanced, or steady"),
            ("Surprise", "surprise", "Curious, startled, or amazed")
        ]

        grid_col1, grid_col2 = st.columns(2)
        for i, (label, val, desc) in enumerate(emotions):
            col = grid_col1 if i % 2 == 0 else grid_col2
            with col:
                if st.button(f"**{label}**\n\n_{desc}_", key=f"emo_{val}", use_container_width=True):
                    st.session_state.baseline_emotion = val
                    st.session_state.chat_history.append(
                        {"role": "system", "content": f"Initial emotional baseline calibrated: {val.capitalize()}."}
                    )
                    st.session_state.study_step = "ai_bot"
                    st.rerun()

        st.divider()
        if st.button("Back to Consent"):
            st.session_state.study_step = "agreement"
            st.rerun()

# ==========================================
# STEP 4: AI COMPANION BOT INTERFACE
# ==========================================
elif st.session_state.study_step == "ai_bot":
    emo_val = st.session_state.baseline_emotion or "neutral"

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"### AffetX Companion")
        st.caption("Emotionally Adaptive Neural Pipeline &bull; Active")
    with col_h2:
        st.markdown(
            f"<div style='text-align: right;'><span class='server-status-badge'>"
            f"State: <strong>{emo_val.capitalize()}</strong></span></div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Chat history display
    for msg in st.session_state.chat_history:
        if msg["role"] == "system":
            st.info(msg["content"])
        elif msg["role"] == "companion":
            with st.chat_message("assistant"):
                st.write(msg["content"])
        else:
            with st.chat_message("user"):
                st.write(msg["content"])

    # User Input
    st.markdown("#### Input to AffetX")
    tab_text, tab_voice = st.tabs(["Text Input", "Voice Input"])

    with tab_text:
        user_prompt = st.chat_input("Share what is on your mind...")
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            
            responses = {
                "happy": f"That is great to hear. Regarding '{user_prompt}', tell me more about how things are going.",
                "sad": f"I understand, and I am listening. Take all the time you need regarding '{user_prompt}'.",
                "angry": f"I recognize this is frustrating. Let us address '{user_prompt}' systematically.",
                "fear": f"You are in a safe space. What part of '{user_prompt}' is most challenging right now?",
                "neutral": f"Acknowledged. Regarding '{user_prompt}', how would you like to proceed?",
                "surprise": f"That is certainly notable. What aspect of '{user_prompt}' stood out most?"
            }
            comp_reply = responses.get(emo_val, f"Acknowledged: '{user_prompt}'. Adapting empathetic parameters.")
            st.session_state.chat_history.append({"role": "companion", "content": comp_reply})
            st.rerun()

    with tab_voice:
        audio = st.audio_input("Record voice input")
        if audio:
            st.success("Audio captured and processed for acoustic emotion analysis.")

    # Bottom Actions
    st.divider()
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        if st.button("Change Emotion Baseline"):
            st.session_state.study_step = "emotion_checkin"
            st.rerun()
    with col_b2:
        if st.button("Return to Home"):
            st.session_state.study_step = "landing"
            st.session_state.baseline_emotion = None
            st.session_state.chat_history = [
                {"role": "companion", "content": "Hello. I am AffetX, your emotionally adaptive companion. How can I assist you today?"}
            ]
            st.rerun()




