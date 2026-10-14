# MAIN ENTRY POINT FOR PROGRAM
"""
app.py - Entry point, router and home page
============================================
Run from the repo root:
    streamlit run app.py

Modules are NOT modified. Each module's entry file is run
as a normal Streamlit script (via runpy) from inside its own folder, so
relative paths such as emails.json / oshc.json keep working.
"""

import base64
import os
import runpy
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path

import streamlit as st

# set_page_config must be the first Streamlit call, and only once per page.
st.set_page_config(
    page_title="Medibank OSHC & Cyber Awareness",
    page_icon="🛡️",
    layout="centered",
)
# Directory definitions
ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
MODULES_DIR = ROOT / "modules"
ICONS_DIR = ROOT / "assets" / "icons"
# Icon delivery: Use custom icon file if it exists, else fallback to generic emoji.
# Custom icons (file in assets/icons). Modules without one keep their emoji.

ICON_FILES = {
    "phishing": "phishguard.png", #Source: openclipart.org/336791, author:sodruls (edited from original)
    "vishing": "vishguard.png", #Source: openclipart.org/16375, author:silverstreak
    "oshc": "oshc.png",
}
def icon_html(page, emoji):
    """Return the custom icon as an <img> if the file exists, else the emoji."""
    filename = ICON_FILES.get(page)
    if filename:
        data = file_as_base64(ASSETS / "icons" / filename)
        if data:
            return f"<img src='data:image/png;base64,{data}' alt=''>"
    return emoji
# ---------------------------------------------------------------
# Where each module lives.
#   page key -> (folder, entry file, mode)
#   mode "script": the file runs top-level Streamlit code (like app.py)
#   mode "render": the file defines render(); it is called after loading
# If oshc/oshc.py defines render() and oshc/app.py is only a launcher,
# change the oshc line to: (MODULES_DIR / "oshc", "oshc.py", "render")
# ---------------------------------------------------------------
MODULE_CONFIG = {
    "phishing": (MODULES_DIR / "PhishGuard", "app.py", "script"),
    "vishing":  (MODULES_DIR / "Vishguard",  "app.py", "script"),
    "oshc":     (MODULES_DIR / "oshc",       "app.py", "script"),
}

# Each module on the home page: page key, icon, title, one-line description,
# what the student does, and whether it is ready to play.
MODULES = [
    ("phishing", "🎣", "Phishing Awareness",
     "Spot the fake email before it spots you.",
     "3 levels · earn badges", True),
    ("vishing", "📞", "Social Engineering Awareness",
     "Audio required for this module, please use headphones or speakers!",
     "Voice-call scenarios", True),
    ("oshc", "🏥", "OSHC Awareness - Health Cover for International Students",
     "What your Overseas Student Health Cover is and how to use it.",
     "Short sections · one question each", True),
]

# ---------------------------------------------------------------
# FUNCTION: init_state()
# PURPOSE: Set up default session_state values on first load only.
# The root only owns "page"; modules manage their own keys.
# ---------------------------------------------------------------
def init_state():
    st.session_state.setdefault("page", "menu")

# ---------------------------------------------------------------
# FUNCTION: go_to(page_name)
# PURPOSE: Switch screens (FR07). Used as an on_click callback so it
# runs BEFORE the rerun.
# ---------------------------------------------------------------
def go_to(page_name):
    st.session_state.page = page_name

def back_to_menu():
    st.session_state.page = "menu"

@contextmanager
def module_context(folder):
    """Run a teammate's script as if it were launched from its own folder."""
    old_cwd = os.getcwd()
    old_path = list(sys.path)
    old_config = st.set_page_config
    old_page = st.Page
    old_switch = st.switch_page
    before = set(sys.modules)

    def _local(p):
        # Streamlit resolves page paths against the ROOT script's folder.
        # Point relative paths at the module's folder when the file exists there.
        if isinstance(p, (str, os.PathLike)) and not os.path.isabs(p):
            candidate = folder / p
            if candidate.exists():
                return str(candidate)
        return p

    def _page(page, *a, **k):
        return old_page(_local(page), *a, **k)

    def _switch(page, *a, **k):
        return old_switch(_local(page), *a, **k)

    st.set_page_config = lambda *a, **k: None   # root already set it
    st.Page = _page
    st.switch_page = _switch
    os.chdir(folder)
    sys.path.insert(0, str(folder))             # so "import content" works
    try:
        yield
    finally:
        st.set_page_config = old_config
        st.Page = old_page
        st.switch_page = old_switch
        os.chdir(old_cwd)
        sys.path[:] = old_path
        folder_resolved = folder.resolve()
        for name in set(sys.modules) - before:
            file = getattr(sys.modules[name], "__file__", None)
            if file:
                try:
                    if Path(file).resolve().is_relative_to(folder_resolved):
                        sys.modules.pop(name, None)
                except (OSError, ValueError):
                    pass

def render_module(page):
    folder, entry, mode = MODULE_CONFIG[page]
    path = folder / entry

    st.button("← Back to menu", key=f"back_{page}", on_click=back_to_menu)

    if not path.exists():
        st.info("This module isn't ready yet.")
        return

    try:
        with module_context(folder):
            if mode == "script":
                # Streamlit runs app files as __main__, so do the same.
                runpy.run_path(str(path), run_name="__main__")
            else:
                ns = runpy.run_path(str(path), run_name=f"mod_{page}")
                ns["render"]()
    except Exception:
        st.error("This module hit an error.")
        st.code(traceback.format_exc())

# ---------------------------------------------------------------
# Helpers for the home page look
# ---------------------------------------------------------------
@st.cache_data
def file_as_base64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except OSError:
        return ""

# STYLISATION FOR HOMEPAGE WITH CSS, INCLUDING CUSTOM FONT
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
.mod-icon img{{height:4rem;width:auto;display:block}}
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
        "<div class='home-privacy'>No personal data is collected. "
        "Nothing you do here is saved.</div>",
        unsafe_allow_html=True,
    )

    columns = st.columns(len(MODULES))
    for column, (page, icon, name, desc, meta, ready) in zip(columns, MODULES):
        with column:
            with st.container(border=True):
                st.markdown(
                    f"<div class='mod-icon'>{icon_html(page, icon)}</div>"
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
                    width="stretch",   # older Streamlit: use_container_width=True
                )

    st.caption(
        "Built for international students. "
        "This is a practice tool developed by students from Swinburne University of Technology."
    )


# ---------------------------------------------------------------
# FUNCTION: main()
# PURPOSE: Read current page and call the matching render function.
# This is the "router" - it replaces needing separate page files.
# ---------------------------------------------------------------
PAGES = {
    "menu": render_menu,
    "phishing": lambda: render_module("phishing"),
    "vishing":  lambda: render_module("vishing"),
    "oshc":     lambda: render_module("oshc"),
}


def main():
    init_state()
    PAGES.get(st.session_state.page, render_menu)()   # unknown page -> home


# ---- SCRIPT ENTRY POINT ----
main()