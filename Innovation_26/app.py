# MAIN ENTRY POINT FOR PROGRAM
"""
app.py - Entry point, router and home page
============================================
Owns: st.session_state setup, the shared home page (FR01), and calling
the right module's render() based on st.session_state.page.

Run from the repo root:
    streamlit run app.py

Reference: Report section 3.3.1 (Application architecture) and
Table 3.4.2 (app.py row).

Streamlit reruns this whole script on every click, so anything that
must survive a click (page, score, question_index, answered list)
lives in st.session_state, not in a normal variable.

Scores: each module keeps its own score (PhishGuard has levels and a
report card, OSHC has a per-quiz score). Nothing is saved to disk and
no personal data is collected.
"""

import base64
import sys
from pathlib import Path

import streamlit as st

# set_page_config must be the first Streamlit call, and only once per page.
st.set_page_config(
    page_title="Medibank OSHC & Cyber Awareness",
    page_icon="🛡️",
    layout="centered",
)

# ---- Make each module folder importable ----
# The modules live in separate folders (modules/phishing, modules/oshc ...)
# so we add those folders to Python's search path before importing.
ROOT = Path(__file__).resolve().parent
for folder in ("ui", "modules/phishing", "modules/oshc", "modules/vishing"):
    path = str(ROOT / folder)
    if path not in sys.path:
        sys.path.insert(0, path)

import phishing  # noqa: E402  (PhishGuard - spot the fake email)
import vishing   # noqa: E402  (voice scams - placeholder for now)
import oshc      # noqa: E402  (Medibank OSHC basics)

ASSETS = ROOT / "assets"

# Each module on the home page: page key, title, one-line description,
# what the student does, and whether it is ready to play.
MODULES = [
    ("phishing", "🎣", "Phishing Awareness",
     "Spot the fake email before it spots you.",
     "3 levels · earn badges", True),
    ("vishing", "📞", "Social Engineering Awareness",
     "Real caller or scammer? Learn the warning signs of phone scams.",
     "Voice-call scenarios", False),
    ("oshc", "🏥", "Medibank OSHC Awareness",
     "What your Overseas Student Health Cover is and how to use it.",
     "Short sections · one question each", True),
]


# ---------------------------------------------------------------
# FUNCTION: init_state()
# PURPOSE: Set up default session_state values on first load only.
# ---------------------------------------------------------------
def init_state():
    # setdefault only fills in missing values, so progress is not
    # reset on every rerun.
    st.session_state.setdefault("page", "menu")
    st.session_state.setdefault("score", 0)
    st.session_state.setdefault("question_index", 0)
    st.session_state.setdefault("answered", [])


# ---------------------------------------------------------------
# FUNCTION: go_to(page_name)
# PURPOSE: Switch screens and reset per-module counters (FR07).
# Used as an on_click callback so it runs BEFORE the rerun.
# ---------------------------------------------------------------
def go_to(page_name):
    st.session_state.page = page_name
    st.session_state.question_index = 0
    st.session_state.answered = []


# ---------------------------------------------------------------
# Helpers for the home page look
# ---------------------------------------------------------------
@st.cache_data
def file_as_base64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except OSError:
        return ""


def home_css():
    font = file_as_base64(ASSETS / "fonts" / "blocky.ttf")
    font_face = (
        "@font-face{font-family:'Blocky';"
        f"src:url(data:font/ttf;base64,{font}) format('truetype');}}"
        if font else ""
    )
    return f"""<style>
{font_face}
.home-logo{{background:#ffffff;border-radius:16px;padding:18px 24px;
  text-align:center;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.home-logo img{{width:220px;max-width:70%}}
.home-title{{font-family:'Blocky',monospace;font-size:1.35rem;line-height:1.6;
  text-align:center;margin:6px 0 10px;color:#E4002B}}
.home-title span{{color:#009FDF}}
.home-sub{{text-align:center;font-size:1.05rem;opacity:.85;margin-bottom:6px}}
.home-privacy{{text-align:center;font-size:.9rem;padding:8px 12px;border-radius:999px;
  border:1px solid rgba(0,159,223,.45);background:rgba(0,159,223,.08);
  width:fit-content;margin:10px auto 22px}}
.mod-icon{{font-size:2rem;line-height:1}}
.mod-name{{font-family:'Blocky',monospace;font-size:.72rem;line-height:1.7;margin:10px 0 6px;min-height:5.1em}}
.mod-desc{{font-size:.95rem;min-height:4.8em}}
.mod-meta{{font-size:.8rem;opacity:.65;margin:6px 0 10px}}
@media (max-width:640px){{.home-title{{font-size:1rem}}.mod-name,.mod-desc{{min-height:0}}}}
</style>"""


# ---------------------------------------------------------------
# FUNCTION: render_menu()
# PURPOSE: Draw the shared starting page (FR01).
# ---------------------------------------------------------------
def render_menu():
    st.markdown(home_css(), unsafe_allow_html=True)

    logo = file_as_base64(ASSETS / "images" / "medibank.png")
    if logo:
        st.markdown(
            f"<div class='home-logo'><img src='data:image/png;base64,{logo}' "
            "alt='Medibank'></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='home-title'>OSHC &amp; <span>Cyber</span> Awareness</div>"
        "<div class='home-sub'>New to Australia? Learn to spot scams and understand "
        "your health cover in a few short, game-style activities.</div>"
        "<div class='home-privacy'>🔒 No personal data is collected. "
        "Nothing you do here is saved.</div>",
        unsafe_allow_html=True,
    )

    columns = st.columns(len(MODULES))
    for column, (page, icon, name, desc, meta, ready) in zip(columns, MODULES):
        with column:
            with st.container(border=True):
                st.markdown(
                    f"<div class='mod-icon'>{icon}</div>"
                    f"<div class='mod-name'>{name}</div>"
                    f"<div class='mod-desc'>{desc}</div>"
                    f"<div class='mod-meta'>{meta}</div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Start" if ready else "Coming soon",
                    key=f"home_{page}",
                    type="primary" if ready else "secondary",
                    disabled=not ready,
                    on_click=go_to,
                    args=(page,),
                    width="stretch",
                )

    st.caption(
        "Built by Group C2 for Medibank international students. "
        "This is a practice tool. Always check Medibank's official website or app."
    )


# ---------------------------------------------------------------
# FUNCTION: main()
# PURPOSE: Read current page and call the matching render function.
# This is the "router" - it replaces needing separate page files.
# ---------------------------------------------------------------
PAGES = {
    "menu": render_menu,
    "phishing": phishing.render,
    "vishing": vishing.render,
    "oshc": oshc.render,
}


def main():
    init_state()
    PAGES.get(st.session_state.page, render_menu)()   # unknown page -> home


# ---- SCRIPT ENTRY POINT ----
main()
