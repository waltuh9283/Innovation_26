"""
oshc.py - Medibank OSHC Awareness module
=========================================
Owns: an introduction screen, plain-language OSHC explainer sections,
each followed by a short comprehension question (FR05), and a results
screen.

Reference: Report section 1.1.3 (Accessibility) and 1.1.1,
Table 3.4.2 (oshc.py row), sections 3.3.1 - 3.3.3.

Flow:  intro  ->  activity (section + question, repeated)  ->  results
The current screen is stored in st.session_state.oshc_stage, the same
single-variable approach app.py uses for st.session_state.page.
"""

import streamlit as st
import os
import content  # content.load_oshc() reads content/oshc.json

#Directory paths for assets (fonts, images, icons)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
# ---------------------------------------------------------------
# STATE HELPERS
# Streamlit reruns the whole script on every click, so anything that
# must survive a click lives in st.session_state.
# ---------------------------------------------------------------
def init_oshc_state():
    """Create this module's state variables the first time it runs."""
    defaults = {
        "oshc_stage": "intro",        # intro | activity | results
        "oshc_index": 0,              # which section the student is on
        "oshc_score": 0,              # session-only score (no storage)
        "oshc_submitted": False,      # has the current question been answered?
        "oshc_last_correct": None,    # result of the most recent answer
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def reset_oshc():
    """Clear all OSHC state (including radio selections) so the
    module starts again from the intro screen."""
    for key in list(st.session_state.keys()):
        if key.startswith("oshc_"):
            del st.session_state[key]


# ---------------------------------------------------------------
# BUTTON CALLBACKS
# Used with on_click so the state change happens BEFORE the rerun.
# This avoids the "I had to click twice" problem.
# ---------------------------------------------------------------
def start_activity():
    st.session_state.oshc_stage = "activity"


def next_question(total):
    st.session_state.oshc_index += 1
    st.session_state.oshc_submitted = False
    st.session_state.oshc_last_correct = None
    if st.session_state.oshc_index >= total:
        st.session_state.oshc_stage = "results"


def return_to_menu():
    reset_oshc()
    st.session_state.page = "menu"   # app.py's router picks this up


def restart():
    reset_oshc()

# ---------------------------------------------------------------
# SCREEN: Introduction (shown on first load)
# ---------------------------------------------------------------
def show_intro(intro, total):
    st.title(intro["title"])
    st.write(intro["text"])
    st.info(intro["note"])
    st.caption(f"{total} sections")
    st.button("Start learning", type="primary", on_click=start_activity)
    st.button("Back to main menu", on_click=return_to_menu)


# ---------------------------------------------------------------
# FUNCTION: show_section(item)
# PURPOSE: Display a short, plain-language explainer of one OSHC
#          concept (e.g. "What is OSHC?", "How do I make a claim?").
# ---------------------------------------------------------------
def show_section(item):
    st.subheader(item["section_title"])
    st.write(item["section_text"])


# ---------------------------------------------------------------
# FUNCTION: comprehension_check(item, total)
# PURPOSE: Ask a short question testing understanding of the
#          section just shown, using st.radio (report 3.3.3).
# ---------------------------------------------------------------
def comprehension_check(item, total):
    index = st.session_state.oshc_index
    st.markdown(f"**{item['question']}**")
    choice = st.radio(
        "Choose one answer:",
        item["options"],
        index=None,                          # nothing pre-selected
        key=f"oshc_choice_{index}",          # unique per question
        disabled=st.session_state.oshc_submitted,
        label_visibility="collapsed",
    )

    if not st.session_state.oshc_submitted:
        # Button stays disabled until the student picks an answer
        if st.button("Check answer", type="primary", disabled=(choice is None)):
            check_answer(choice, item)
            st.rerun()
    else:
        # Feedback, then a button to move on
        if st.session_state.oshc_last_correct:
            st.success("Correct! " + item["explanation"])
        else:
            st.error("Not quite. " + item["explanation"])
        label = "See my results" if index + 1 >= total else "Next"
        st.button(label, type="primary", on_click=next_question, args=(total,))

# ---------------------------------------------------------------
# FUNCTION: check_answer(choice, item)
# PURPOSE: Compare selection to item["correct_option"], update
#          session score (FR03, FR06).
# ---------------------------------------------------------------
def check_answer(choice, item):
    is_correct = (choice == item["correct_option"])
    if is_correct:
        st.session_state.oshc_score += 1
    st.session_state.oshc_submitted = True
    st.session_state.oshc_last_correct = is_correct
    return is_correct

# ---------------------------------------------------------------
# SCREEN: Results
# ---------------------------------------------------------------
def show_results(total):
    score = st.session_state.oshc_score
    st.title("Well done!")
    st.metric("Your score", f"{score} / {total}")
    if score == total:
        st.success("Perfect score. You understand the OSHC basics.")
    else:
        st.write("Good effort. You can try again to improve your score.")
    st.button("Try again", on_click=restart)
    st.button("Back to main menu", type="primary", on_click=return_to_menu)


# ---------------------------------------------------------------
# FUNCTION: render()
# PURPOSE: Main entry point, called by app.py's router when
#          st.session_state.page == "oshc".
# ---------------------------------------------------------------
def render():
    init_oshc_state()
    data = content.load_oshc()
    items = data["sections"]
    total = len(items)
    stage = st.session_state.oshc_stage

    if stage == "intro":
        show_intro(data["intro"], total)

    elif stage == "activity":
        index = st.session_state.oshc_index
        st.progress((index + 1) / total, text=f"Section {index + 1} of {total}")
        show_section(items[index])
        comprehension_check(items[index], total)
        st.divider()
        #ADD FUNCTIONALITY LATER - RETURN TO MAIN MENU BUTTON
        st.button("Return to main menu", on_click=return_to_menu)

    else:
        show_results(total)

# To run module: streamlit run oshc.py
if __name__ == "__main__":
    render()
