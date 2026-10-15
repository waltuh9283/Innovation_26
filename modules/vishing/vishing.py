"""VishGuard - Cybersecurity Awareness Simulator."""
#CLONE OF PHISHGUARD - CHANGE ACCORDINGLY
import pygame, sys, json, random, os
pygame.init()
"""
vishing.py - Voice Phishing / Social Engineering module
==========================================================
Owns: playing a voice clip and asking the student to judge whether
it is a genuine caller or an AI-generated/suspicious voice (FR04).

Reference: Report section 1.1.1 and 3.3.4 (Audio),
Table 3.4.2 (vishing.py row).
"""

# ---- IMPORTS (pseudocode) ----
# import streamlit as st
# import content
# import ui


# ---------------------------------------------------------------
# FUNCTION: render()
# PURPOSE: Main entry point, called by app.py's router when
#          st.session_state.page == "vishing".
# ---------------------------------------------------------------
def render():
    # items = content.load_vishing()
    # total = LENGTH of items
    # index = st.session_state.question_index
    #
    # IF index >= total:
    #     CALL ui.results_screen(st.session_state.score, total, "Social Engineering Awareness")
    #     RETURN
    #
    # current_item = items[index]
    #
    # CALL ui.progress_bar(index + 1, total)
    # CALL play_clip(current_item["audio_filename"])
    #
    # DISPLAY buttons: "Genuine" / "AI-generated / Suspicious"
    # IF student selects an answer:
    #     CALL check_answer(choice, current_item)
    #     CALL show_explanation(current_item)
    #     CALL ui.next_button()
    #
    # CALL ui.return_button()
    pass


# ---------------------------------------------------------------
# FUNCTION: play_clip(filename)
# PURPOSE: Play the local audio clip via st.audio. User-triggered,
#          not autoplay (browsers block autoplay by default - 3.3.4).
# ---------------------------------------------------------------
def play_clip(filename):
    # path = "audio/" + filename
    # CALL st.audio(path)
    pass


# ---------------------------------------------------------------
# FUNCTION: check_answer(choice, item)
# PURPOSE: Compare student's judgement to item["is_genuine"],
#          update session score (FR03, FR06).
# ---------------------------------------------------------------
def check_answer(choice, item):
    # is_correct = (choice == item["is_genuine"])
    # IF is_correct:
    #     INCREMENT st.session_state.score
    # APPEND is_correct to st.session_state.answered
    # RETURN is_correct
    pass


# ---------------------------------------------------------------
# FUNCTION: show_explanation(item)
# PURPOSE: Explain WHY the clip was genuine or suspicious, e.g.
#          urgency, authority, unusual request for personal info.
# ---------------------------------------------------------------
def show_explanation(item):
    # DISPLAY item["explanation"]
    pass