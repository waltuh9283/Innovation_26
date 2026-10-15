import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Load CSS
css_file = BASE_DIR / "static" / "css" / "style.css"

css = css_file.read_text(encoding="utf-8")

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

# Load HTML
html_file = BASE_DIR / "templates" / "home.html"

html = html_file.read_text(encoding="utf-8")

st.markdown(
    html,
    unsafe_allow_html=True
)

# Welcome audio
welcome_audio = BASE_DIR / "static" / "audio" / "welcome.mp3"

if welcome_audio.exists():
    st.audio(str(welcome_audio), autoplay=True)
else:
    st.info("Welcome audio will appear here once added.")

# Keep navigation as Streamlit buttons
st.subheader("🎮 Choose Your Level")

if st.button("🟢 Beginner", use_container_width=True):
    st.switch_page("beginner/beginner.py")

if st.button("🟡 Intermediate", use_container_width=True):
    st.switch_page("intermediate/intermediate.py")

if st.button("🔴 Advanced", use_container_width=True):
    st.info("Advanced level coming soon!")