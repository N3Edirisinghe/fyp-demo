import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# =========================================================
# STREAMLIT CLOUD APP CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AffetX — Emotionally Adaptive AI Companion",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Responsive full-bleed styling
st.markdown("""
    <style>
        #MainMenu {visibility: hidden !important;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none;
            width: 100vw;
            height: 100vh;
            min-height: 100vh;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

def get_bundled_html():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(base_dir, "frontend")
    
    html_path = os.path.join(frontend_dir, "index.html")
    css_path = os.path.join(frontend_dir, "css", "styles.css")
    js_path = os.path.join(frontend_dir, "js", "main.js")
    img_path = os.path.join(frontend_dir, "assets", "blue_jay_bird.jpg")

    html_content = ""
    css_content = ""
    js_content = ""

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

    # Convert bird image to Base64 URI so it renders seamlessly anywhere
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{b64_img}"
            html_content = html_content.replace('src="assets/blue_jay_bird.jpg"', f'src="{data_uri}"')

    # Bundle CSS and JS directly inside HTML
    if css_content:
        html_content = html_content.replace('<link rel="stylesheet" href="css/styles.css">', f'<style>{css_content}</style>')
    if js_content:
        html_content = html_content.replace('<script src="js/main.js"></script>', f'<script>{js_content}</script>')

    return html_content

# Render Fullscreen AffetX Companion
bundled_html = get_bundled_html()

if bundled_html:
    components.html(bundled_html, height=920, scrolling=False)
else:
    st.error("Frontend bundle initializing. Please ensure the frontend folder is present in the repository.")
