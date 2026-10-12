# MAIN ENTRY POINT FOR PROGRAM
"""
app.py - Entry point and router
=================================
Owns: st.session_state setup, top-level navigation, calling the right
module's render() based on session_state.page.

Reference: Report section 3.3.1 (Application architecture) and
Table 3.4.2 (app.py row).

Streamlit reruns this whole script on every click, so anything that
must survive a click (page, score, question_index, answered list)
lives in st.session_state, not in a normal variable.
"""

# ---- IMPORTS (pseudocode) ----
# import streamlit as st
# import content        # load_phishing, load_vishing, load_oshc
# import ui              # shared components
# import phishing
# import vishing
# import oshc


# ---------------------------------------------------------------
# FUNCTION: init_state()
# PURPOSE: Set up default session_state values on first load only.
# ---------------------------------------------------------------
def init_state():
    # IF "page" is not already in st.session_state:
    #     st.session_state.page = "menu"
    #     st.session_state.score = 0
    #     st.session_state.question_index = 0
    #     st.session_state.answered = []      # list of bools/records per question
    #
    # NOTE: only set defaults if missing, so we don't reset progress
    # on every rerun (Streamlit reruns constantly).
    pass


# ---------------------------------------------------------------
# FUNCTION: render_menu()
# PURPOSE: Draw the shared starting page (FR01).
# ---------------------------------------------------------------
def render_menu():
    # DISPLAY title ("Medibank OSHC & Cyber Awareness")
    # DISPLAY short 1-2 sentence explainer of what the app is and does
    # DISPLAY privacy statement: "No personal data is collected."
    #
    # CREATE three buttons, one per module:
    #     IF button "Phishing Awareness" clicked:
    #         CALL go_to("phishing")
    #     IF button "Social Engineering Awareness" clicked:
    #         CALL go_to("vishing")
    #     IF button "Medibank OSHC Awareness" clicked:
    #         CALL go_to("oshc")
    pass


# ---------------------------------------------------------------
# FUNCTION: go_to(page_name)
# PURPOSE: Switch screens and reset per-module counters (FR07).
# ---------------------------------------------------------------
def go_to(page_name):
    # SET st.session_state.page = page_name
    # SET st.session_state.question_index = 0
    # SET st.session_state.answered = []
    # (score can either reset here or persist across modules -
    #  TEAM DECISION: confirm behaviour before building ui.score_counter)
    # CALL st.rerun()   # force immediate redraw with new page value
    pass


# ---------------------------------------------------------------
# FUNCTION: main()
# PURPOSE: Read current page and call the matching render function.
# This is the "router" - it replaces needing separate page files.
# ---------------------------------------------------------------
def main():
    # CALL init_state()
    #
    # SWITCH on st.session_state.page:
    #     CASE "menu":     CALL render_menu()
    #     CASE "phishing": CALL phishing.render()
    #     CASE "vishing":  CALL vishing.render()
    #     CASE "oshc":     CALL oshc.render()
    #     DEFAULT:         CALL render_menu()   # fallback / unknown state
    pass


# ---- SCRIPT ENTRY POINT ----
# IF this file is run directly (streamlit run app.py):
#     CALL main()