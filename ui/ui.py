#Main UI Python module
"""
ui.py - Shared components used by all three modules
======================================================
Owns: the reusable Streamlit widgets that phishing.py, vishing.py and
oshc.py all need, so scoring/feedback/navigation UI is written once
and looks consistent across modules.

Reference: Report section 3.3.3 (Interface) and
Table 3.4.2 (ui.py row).
"""

# ---- IMPORTS (pseudocode) ----
# import streamlit as st


# ---------------------------------------------------------------
# FUNCTION: score_counter()
# PURPOSE: Show current score and how many questions answered so far.
# ---------------------------------------------------------------
def score_counter():
    # answered_count = LENGTH of st.session_state.answered
    # DISPLAY "Score: {st.session_state.score} / {answered_count}"
    pass


# ---------------------------------------------------------------
# FUNCTION: progress_bar(current, total)
# PURPOSE: Show position within the current module (NFR01/02).
# ---------------------------------------------------------------
def progress_bar(current, total):
    # fraction = current / total   # guard against divide-by-zero if total == 0
    # CALL st.progress(fraction)
    # DISPLAY "Question {current} of {total}"
    pass


# ---------------------------------------------------------------
# FUNCTION: next_button()
# PURPOSE: Advance to the next scenario within the module.
# ---------------------------------------------------------------
def next_button():
    # IF st.button("Next") clicked:
    #     INCREMENT st.session_state.question_index
    #     CLEAR any stored feedback/selection for the current question
    #     CALL st.rerun()
    pass


# ---------------------------------------------------------------
# FUNCTION: return_button()
# PURPOSE: Let the student return to the shared home page (FR07).
# ---------------------------------------------------------------
def return_button():
    # IF st.button("Return to menu") clicked:
    #     SET st.session_state.page = "menu"
    #     CALL st.rerun()
    pass


# ---------------------------------------------------------------
# FUNCTION: feedback_box(correct, explanation)
# PURPOSE: Show immediate right/wrong feedback (FR03).
# ---------------------------------------------------------------
def feedback_box(correct, explanation):
    # IF correct is True:
    #     DISPLAY green box: "Correct! " + explanation
    # ELSE:
    #     DISPLAY red box: "Not quite. " + explanation
    pass


# ---------------------------------------------------------------
# FUNCTION: results_screen(score, total, module_name)
# PURPOSE: End-of-module summary, shown after the last scenario.
# ---------------------------------------------------------------
def results_screen(score, total, module_name):
    # DISPLAY heading: "{module_name} complete!"
    # DISPLAY "You scored {score} out of {total}"
    # CALL return_button()
    pass