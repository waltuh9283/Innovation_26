
import streamlit as st
from pathlib import Path


# HOME PAGE - OVERALL SCORES


beginner_score = st.session_state.get("beginner_score", 0)
intermediate_score = st.session_state.get("intermediate_score", 0)
advanced_score = st.session_state.get("game_score", 0)

overall_score = (
    beginner_score
    + intermediate_score
    + advanced_score
)


# LEVEL COMPLETION TRACKING


beginner_done = st.session_state.get(
    "beginner_completed", False
)

intermediate_done = st.session_state.get(
    "intermediate_completed", False
)

advanced_done = st.session_state.get(
    "advanced_completed", False
)

completed_levels = sum([
    beginner_done,
    intermediate_done,
    advanced_done
])


# OVERALL SCORE DISPLAY


st.subheader("🏆 Overall Game Score")

st.metric(
    "Total Score",
    f"{overall_score}/120"
)

st.progress(min(overall_score / 120, 1.0))



# MODULE COMPLETION POP-UP


@st.dialog("🏆 Vishing Awareness Module Completed!")
def show_completion_popup():

    st.balloons()

    st.success(
        "🎉 Congratulations! You have successfully "
        "completed all three levels!"
    )

    st.markdown("### 🌟 Perfect Score: 120/120")

    st.write(
        "Excellent work! You have demonstrated "
        "your ability to recognise vishing scams "
        "and protect sensitive information."
    )

    if st.button("🎉 Awesome!", use_container_width=True):
        st.session_state.completion_popup_shown = True
        st.rerun()



# CHECK OVERALL SCORE


if overall_score == 120:

    st.success(
        "🏆 Congratulations! You have successfully "
        "completed the Vishing Awareness Module "
        "with a perfect score of 120/120!"
    )

    # Show popup only once
    if not st.session_state.get("completion_popup_shown", False):
        show_completion_popup()

else:

    # Allow popup to appear again after a new perfect score
    st.session_state.completion_popup_shown = False

    st.info(
        f"🎮 Keep practising! Your current score is "
        f"{overall_score}/120. "
        f"Complete the module by achieving 120/120."
    )

    st.caption(f"Levels played: {completed_levels}/3")

BASE_DIR = Path(__file__).resolve().parent



# HOME PAGE BACKGROUND MUSIC

BACKGROUND_MUSIC = (
    BASE_DIR / "static" / "sounds" / "background.mp3"
)

if BACKGROUND_MUSIC.exists():

    st.audio(
        BACKGROUND_MUSIC.read_bytes(),
        format="audio/mpeg",
        autoplay=True,
        loop=True
    )

else:
    st.warning("Background music file not found.")



# VICTORY SOUND


VICTORY_SOUND = BASE_DIR / "static" / "sounds" / "victory.mp3"

def play_victory_sound():
    if VICTORY_SOUND.exists():
        st.audio(
            VICTORY_SOUND.read_bytes(),
            format="audio/mpeg",
            autoplay=True
        )
    else:
        st.warning("Victory sound file not found.")



# LOAD CSS AND HTML


BASE_DIR = Path(__file__).resolve().parent

# Load CSS
css_file = BASE_DIR / "static" / "css" / "style.css"

if css_file.exists():

    css = css_file.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )

# Load HTML
html_file = BASE_DIR / "templates" / "home.html"

if html_file.exists():

    html = html_file.read_text(encoding="utf-8")

    st.markdown(
        html,
        unsafe_allow_html=True
    )

# WELCOME AUDIO


welcome_audio = (
    BASE_DIR / "static" / "audio" / "welcome.mp3"
)

if welcome_audio.exists():

    st.audio(
        str(welcome_audio),
        autoplay=True
    )

else:

    st.info(
        "Welcome audio will appear here once added."
    )



# CHOOSE YOUR LEVEL


st.subheader("🎮 Choose Your Level")

# Beginner Level
if st.button(
    f"🟢 Beginner                         {beginner_score}/40",
    use_container_width=True,
    key="home_beginner"
):

    st.switch_page("beginner/beginner.py")


# Intermediate Level
if st.button(
    f"🟡 Intermediate                     {intermediate_score}/40",
    use_container_width=True,
    key="home_intermediate"
):

    st.switch_page("intermediate/intermediate.py")


# Advanced Level
if st.button(
    f"🔴 Advanced                         {advanced_score}/40",
    use_container_width=True,
    key="home_advanced"
):

    st.switch_page("Advanced/advanced.py")
