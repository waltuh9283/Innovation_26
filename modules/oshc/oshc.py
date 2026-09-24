"""VishGuard - Cybersecurity Awareness Simulator."""
#CLONE OF PHISHGUARD - CHANGE ACCORDINGLY
import pygame, sys, json, random, os  
pygame.init()

"""
oshc.py - Medibank OSHC Awareness module
==========================================
Owns: plain-language OSHC explainer sections, each followed by a
short comprehension question (FR05).

Reference: Report section 1.1.3 (Accessibility) and 1.1.1,
Table 3.4.2 (oshc.py row).
"""

# ---- IMPORTS (pseudocode) ----
# import streamlit as st
# import content
# import ui


# ---------------------------------------------------------------
# FUNCTION: render()
# PURPOSE: Main entry point, called by app.py's router when
#          st.session_state.page == "oshc".
# ---------------------------------------------------------------
def render():
    # items = content.load_oshc()
    # total = LENGTH of items
    # index = st.session_state.question_index
    #
    # IF index >= total:
    #     CALL ui.results_screen(st.session_state.score, total, "Medibank OSHC Awareness")
    #     RETURN
    #
    # current_item = items[index]
    #
    # CALL ui.progress_bar(index + 1, total)
    # CALL show_section(current_item)
    # CALL comprehension_check(current_item)
    #
    # CALL ui.return_button()
    pass


# ---------------------------------------------------------------
# FUNCTION: show_section(item)
# PURPOSE: Display a short, plain-language explainer of one OSHC
#          concept (e.g. "What is OSHC?", "How do I make a claim?").
# ---------------------------------------------------------------
def show_section(item):
    # DISPLAY item["section_text"]
    # (keep language simple - target users have varied English
    #  proficiency, per report section 3.2.2)
    pass


# ---------------------------------------------------------------
# FUNCTION: comprehension_check(item)
# PURPOSE: Ask a short question testing understanding of the
#          section just shown, using st.radio (report 3.3.3).
# ---------------------------------------------------------------
def comprehension_check(item):
    # DISPLAY item["question"]
    # choice = st.radio(options = item["options"])
    #
    # IF student submits an answer:
    #     CALL check_answer(choice, item)
    #     CALL ui.next_button()
    pass


# ---------------------------------------------------------------
# FUNCTION: check_answer(choice, item)
# PURPOSE: Compare selection to item["correct_option"], update
#          session score (FR03, FR06), show feedback via ui module.
# ---------------------------------------------------------------
def check_answer(choice, item):
    # is_correct = (choice == item["correct_option"])
    # IF is_correct:
    #     INCREMENT st.session_state.score
    # APPEND is_correct to st.session_state.answered
    # CALL ui.feedback_box(is_correct, item["explanation"])
    # RETURN is_correct
    pass