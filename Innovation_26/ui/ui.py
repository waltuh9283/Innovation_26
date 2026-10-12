#Main UI Python module
"""
ui.py - Shared components used by all three modules
======================================================
Owns: the reusable Streamlit widgets that phishing.py, vishing.py and
oshc.py all need, so scoring/feedback/navigation UI is written once
and looks consistent across modules.

Reference: Report section 3.3.3 (Interface) and
Table 3.4.2 (ui.py row).

Buttons use on_click callbacks so the state change happens BEFORE the
rerun (avoids the "had to click twice" problem).
"""

import streamlit as st


def _go_menu():
    st.session_state.page = "menu"


def _next_question():
    st.session_state.question_index = st.session_state.get("question_index", 0) + 1


# ---------------------------------------------------------------
# FUNCTION: score_counter()
# PURPOSE: Show current score and how many questions answered so far.
# ---------------------------------------------------------------
def score_counter():
    answered_count = len(st.session_state.get("answered", []))
    st.markdown(f"**Score: {st.session_state.get('score', 0)} / {answered_count}**")


# ---------------------------------------------------------------
# FUNCTION: progress_bar(current, total)
# PURPOSE: Show position within the current module (NFR01/02).
# ---------------------------------------------------------------
def progress_bar(current, total):
    fraction = current / total if total else 0
    st.progress(min(max(fraction, 0.0), 1.0), text=f"Question {current} of {total}")


# ---------------------------------------------------------------
# FUNCTION: next_button()
# PURPOSE: Advance to the next scenario within the module.
# ---------------------------------------------------------------
def next_button(key="ui_next"):
    st.button("Next", type="primary", key=key, on_click=_next_question)


# ---------------------------------------------------------------
# FUNCTION: return_button()
# PURPOSE: Let the student return to the shared home page (FR07).
# ---------------------------------------------------------------
def return_button(key="ui_return"):
    st.button("🏠 Back to home", key=key, on_click=_go_menu)


# ---------------------------------------------------------------
# FUNCTION: feedback_box(correct, explanation)
# PURPOSE: Show immediate right/wrong feedback (FR03).
# ---------------------------------------------------------------
def feedback_box(correct, explanation):
    if correct:
        st.success("Correct! " + explanation)
    else:
        st.error("Not quite. " + explanation)


# ---------------------------------------------------------------
# FUNCTION: results_screen(score, total, module_name)
# PURPOSE: End-of-module summary, shown after the last scenario.
# ---------------------------------------------------------------
def results_screen(score, total, module_name):
    st.title(f"{module_name} complete!")
    st.metric("Your score", f"{score} / {total}")
    return_button(key="ui_results_return")
