"""
oshc.py - Medibank OSHC Awareness module (upgraded)
====================================================
Self-contained module: run alone with `streamlit run oshc.py`, or imported by
the hub's app.py, which calls render() when st.session_state.page == "oshc".

Upgrades: dark cyber theme (matches PhishGuard), XP + streak multiplier,
a 50/50 lifeline, shuffled answers, and a results screen with an
OSHC Readiness gauge, badges and a review of missed questions.
"""
import html
import os
import random

import plotly.graph_objects as go
import streamlit as st

import content  # content.load_oshc() reads oshc.json next to this file

# Directory paths for assets (fonts, images, icons)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "assets", "images")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")
LOGO = os.path.join(IMAGES_DIR, "medibank.png")

FIFTY_COST = 3  # XP cost of using the 50/50 lifeline

CSS = """<style>
.stApp{background:radial-gradient(circle at 20% 0%,#10224a 0%,#070b17 60%);color:#e6f1ff}
h1,h2,h3{font-family:'Courier New',monospace}
.title{font-size:2.3rem;font-weight:800;font-family:'Courier New',monospace;background:linear-gradient(90deg,#00e5ff,#7c4dff);-webkit-background-clip:text;color:transparent}
.hud{display:flex;gap:8px;margin:4px 0 12px}
.box{flex:1;background:#0d1530;border:1px solid #1f3a6e;border-radius:12px;padding:6px;text-align:center;box-shadow:0 0 12px #00e5ff22}
.box small{color:#7f9cc9;display:block}.box b{font-size:1.3rem;color:#00e5ff;display:inline-block}
.pop{animation:pop .6s}@keyframes pop{0%{transform:scale(1.8);color:#fff}100%{transform:scale(1)}}
.card{background:#0d1530;border:1px solid #2a4a8a;border-left:4px solid #00e5ff;border-radius:10px;padding:14px 16px;margin:8px 0}
.ok{border-left-color:#00e676;background:#0b2a1c}
.bad{border-left-color:#ff1744;background:#2a0b14;animation:glitch .7s}
@keyframes glitch{0%,100%{transform:translate(0)}10%{transform:translate(-6px,2px);filter:hue-rotate(90deg)}30%{transform:translate(6px,-2px)}50%{transform:translate(-4px,0);filter:hue-rotate(-90deg)}70%{transform:translate(3px,2px)}}
.badge{display:inline-block;margin:4px;padding:8px 12px;border-radius:20px;border:1px solid #00e5ff;background:#0d1530}
.badge.off{opacity:.3;border-color:#555}
</style>"""


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
        "oshc_score": 0,              # XP (session-only, nothing is stored)
        "oshc_streak": 0,             # correct answers in a row
        "oshc_best": 0,               # best streak this run
        "oshc_submitted": False,      # has the current question been answered?
        "oshc_last_correct": None,    # result of the most recent answer
        "oshc_last_pts": 0,           # XP earned by the most recent answer
        "oshc_last_mult": 1.0,        # multiplier used for it
        "oshc_fifty_used": False,     # 50/50 lifeline is once per run
        "oshc_orders": {},            # question index -> shuffled options
        "oshc_fifty": {},             # question index -> the 2 options kept
        "oshc_log": [],               # one record per answered question
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def reset_oshc():
    """Clear all OSHC state (including radio selections) so the
    module starts again from the intro screen."""
    for key in list(st.session_state.keys()):
        if key.startswith("oshc_"):
            del st.session_state[key]


def multiplier():
    return min(1 + 0.25 * st.session_state.oshc_streak, 2.0)


# ---------------------------------------------------------------
# BUTTON CALLBACKS
# Used with on_click so the state change happens BEFORE the rerun.
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


def use_fifty(item, index):
    """50/50 lifeline: keep the correct answer plus one random wrong one."""
    wrong = [o for o in item["options"] if o != item["correct_option"]]
    st.session_state.oshc_fifty[index] = [item["correct_option"], random.choice(wrong)]
    st.session_state.oshc_fifty_used = True
    st.session_state.oshc_score = max(0, st.session_state.oshc_score - FIFTY_COST)


# ---------------------------------------------------------------
# UI PIECES
# ---------------------------------------------------------------
def hud(total):
    s = st.session_state
    pop = "pop" if s.oshc_submitted and s.oshc_last_correct else ""
    done = len(s.oshc_log)
    right = sum(1 for r in s.oshc_log if r["correct"])
    st.markdown(f"""<div class='hud'>
    <div class='box'><small>XP</small><b class='{pop}'>{s.oshc_score}</b></div>
    <div class='box'><small>STREAK 🔥</small><b>{s.oshc_streak}</b></div>
    <div class='box'><small>MULTIPLIER</small><b>x{multiplier():.2f}</b></div>
    <div class='box'><small>CORRECT</small><b>{right}/{done}</b></div></div>""",
                unsafe_allow_html=True)


# ---------------------------------------------------------------
# SCREEN: Introduction (shown on first load)
# ---------------------------------------------------------------
def show_intro(intro, total):
    if os.path.exists(LOGO):
        st.image(LOGO, width=170)
    st.markdown(f"<div class='title'>{html.escape(intro['title'])}</div>", unsafe_allow_html=True)
    st.write(intro["text"])
    st.info(intro["note"])
    with st.expander("How scoring works"):
        st.markdown("- Each correct answer earns **10 XP x your streak multiplier**.\n"
                    "- Every answer in a row adds +0.25 to the multiplier (max x2.00).\n"
                    f"- One **50/50 lifeline** per run removes two wrong answers (costs {FIFTY_COST} XP).\n"
                    "- Wrong answers cost nothing. You just see the explanation and learn.")
    st.caption(f"{total} sections")
    st.button("Start learning", type="primary", on_click=start_activity)
    st.button("Back to main menu", on_click=return_to_menu)


# ---------------------------------------------------------------
# FUNCTION: show_section(item)
# PURPOSE: Display a short, plain-language explainer of one OSHC concept.
# ---------------------------------------------------------------
def show_section(item):
    st.subheader(item["section_title"])
    st.markdown(f"<div class='card'>{html.escape(item['section_text'])}</div>", unsafe_allow_html=True)


def get_options(item, index):
    """Shuffled once per question (stable across reruns), narrowed by 50/50."""
    s = st.session_state
    if index not in s.oshc_orders:
        opts = list(item["options"])
        random.shuffle(opts)
        s.oshc_orders[index] = opts
    opts = s.oshc_orders[index]
    if index in s.oshc_fifty:
        opts = [o for o in opts if o in s.oshc_fifty[index]]
    return opts


# ---------------------------------------------------------------
# FUNCTION: comprehension_check(item, total)
# PURPOSE: Ask a short question testing understanding of the section.
# ---------------------------------------------------------------
def comprehension_check(item, total):
    s = st.session_state
    index = s.oshc_index
    st.markdown(f"**{item['question']}**")
    choice = st.radio(
        "Choose one answer:",
        get_options(item, index),
        index=None,                          # nothing pre-selected
        key=f"oshc_choice_{index}",          # unique per question
        disabled=s.oshc_submitted,
        label_visibility="collapsed",
    )

    if not s.oshc_submitted:
        c1, c2 = st.columns(2)
        if c1.button("Check answer", type="primary", disabled=(choice is None), width="stretch"):
            check_answer(choice, item)
            st.rerun()
        c2.button(f"🎯 50/50 (-{FIFTY_COST} XP)", width="stretch",
                  disabled=s.oshc_fifty_used, on_click=use_fifty, args=(item, index))
    else:
        exp = html.escape(item["explanation"])
        if s.oshc_last_correct:
            st.markdown(f"<div class='card ok'><b>✅ Correct! +{s.oshc_last_pts} XP "
                        f"(x{s.oshc_last_mult:.2f})</b><br>{exp}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='card bad'><b>❌ Not quite.</b><br>{exp}</div>",
                        unsafe_allow_html=True)
        label = "See my results" if index + 1 >= total else "Next"
        st.button(label, type="primary", on_click=next_question, args=(total,))


# ---------------------------------------------------------------
# FUNCTION: check_answer(choice, item)
# PURPOSE: Compare selection to item["correct_option"], update XP and streak.
# ---------------------------------------------------------------
def check_answer(choice, item):
    s = st.session_state
    is_correct = (choice == item["correct_option"])
    mult = multiplier()
    pts = 0
    if is_correct:
        pts = round(10 * mult)
        s.oshc_score += pts
        s.oshc_streak += 1
        s.oshc_best = max(s.oshc_best, s.oshc_streak)
    else:
        s.oshc_streak = 0
    s.oshc_submitted = True
    s.oshc_last_correct = is_correct
    s.oshc_last_pts, s.oshc_last_mult = pts, mult
    s.oshc_log.append(dict(title=item["section_title"], correct=is_correct, chosen=choice,
                           answer=item["correct_option"], explanation=item["explanation"]))
    return is_correct


# ---------------------------------------------------------------
# SCREEN: Results
# ---------------------------------------------------------------
def show_results(total):
    s = st.session_state
    log = s.oshc_log
    right = sum(1 for r in log if r["correct"])
    pct = round(100 * right / total) if total else 0
    rank = ("OSHC Expert" if pct >= 90 else "Confident" if pct >= 70
            else "Getting there" if pct >= 50 else "Needs revision")

    st.markdown("<div class='title'>Well done!</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct, number={"suffix": "%"}, title={"text": "OSHC Readiness"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#00e5ff"},
               "steps": [{"range": [0, 50], "color": "#5c1020"}, {"range": [50, 80], "color": "#5c4a10"},
                         {"range": [80, 100], "color": "#0b3a24"}]}))
    fig.update_layout(template="plotly_dark", height=280, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=60, b=0))
    st.plotly_chart(fig, width="stretch")

    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{right} / {total}")
    c2.metric("XP", s.oshc_score)
    c3.metric("Best streak", s.oshc_best)
    st.markdown(f"**Rank: {rank}**")

    if right == total:
        st.success("Perfect score. You understand the OSHC basics.")
    else:
        st.write("Good effort. Review the topics below, then try again to improve.")

    badges = [("🏥 OSHC Expert", pct >= 90, "90% or more correct"),
              ("🔥 Streak Master", s.oshc_best >= 5, "5 correct in a row"),
              ("🎯 Flawless", right == total, "Every answer correct"),
              ("🧠 No Lifelines", (not s.oshc_fifty_used) and pct >= 75, "75%+ without using 50/50"),
              ("🛡️ Scam Spotter", bool(log) and log[-1]["correct"], "Got the fake-message question right")]
    st.markdown("### 🏅 Badges")
    st.markdown("".join(f"<span class='badge {'' if ok else 'off'}' title='{d}'>{b}</span>"
                        for b, ok, d in badges), unsafe_allow_html=True)

    missed = [r for r in log if not r["correct"]]
    if missed:
        st.markdown("### 📚 Review what you missed")
        for r in missed:
            with st.expander(r["title"]):
                st.markdown(f"**Your answer:** {r['chosen']}  \n**Correct answer:** {r['answer']}")
                st.info(r["explanation"])

    st.button("Try again", on_click=restart, width="stretch")
    st.button("Back to main menu", type="primary", on_click=return_to_menu, width="stretch")


# ---------------------------------------------------------------
# FUNCTION: render()
# PURPOSE: Main entry point, called by app.py's router when
#          st.session_state.page == "oshc".
# ---------------------------------------------------------------
def render():
    st.markdown(CSS, unsafe_allow_html=True)
    init_oshc_state()
    data = content.load_oshc()
    items = data["sections"]
    total = len(items)
    stage = st.session_state.oshc_stage

    if stage == "intro":
        show_intro(data["intro"], total)

    elif stage == "activity":
        index = st.session_state.oshc_index
        hud(total)
        st.progress((index + 1) / total, text=f"Section {index + 1} of {total}")
        show_section(items[index])
        comprehension_check(items[index], total)
        st.divider()
        st.button("Return to main menu", on_click=return_to_menu)

    else:
        show_results(total)


# To run module: streamlit run oshc.py
if __name__ == "__main__":
    st.set_page_config(page_title="Medibank OSHC Basics", page_icon="🏥", layout="centered")
    render()