"""PhishGuard: OSHC Cyber Defence (Streamlit). Run: streamlit run app.py"""
import json, random, time, html
from pathlib import Path
from urllib.parse import urlparse
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="PhishGuard · OSHC Cyber Defence", page_icon="🛡️", layout="centered")
S = st.session_state
TIME = 25
PARTS = ["sender", "greeting", "body", "link"]
LEVELS = {
    1: ("Orientation Week", "Welcome to Melbourne! Scammers target new students first. Spot the obvious ones.", 45),
    2: ("Student Life", "Visa, OSHC claims, rent and uni portals. Real life is full of lookalikes.", 60),
    3: ("Targeted Attack", "They know your name and your cover dates. Only the details give them away.", 70),
}
CATS = {"urgency": "Urgency pressure", "domain": "Fake / lookalike domain", "lure": "Too good to be true",
        "impersonation": "Impersonation", "credential": "Credential theft", "legit": "Recognising safe mail"}
TWO_PART = {"com.au", "edu.au", "gov.au", "org.au", "net.au", "com.co", "vic.gov.au"}

CSS = """<style>
.stApp{background:radial-gradient(circle at 20% 0%,#10224a 0%,#070b17 60%);color:#e6f1ff}
h1,h2,h3{font-family:'Courier New',monospace}
.title{font-size:2.6rem;font-weight:800;font-family:'Courier New',monospace;background:linear-gradient(90deg,#00e5ff,#7c4dff);-webkit-background-clip:text;color:transparent}
.hud{display:flex;gap:8px;margin:4px 0 12px}
.box{flex:1;background:#0d1530;border:1px solid #1f3a6e;border-radius:12px;padding:6px;text-align:center;box-shadow:0 0 12px #00e5ff22}
.box small{color:#7f9cc9;display:block}.box b{font-size:1.35rem;color:#00e5ff;display:inline-block}
.pop{animation:pop .6s}@keyframes pop{0%{transform:scale(1.8);color:#fff}100%{transform:scale(1)}}
.mail{background:#0d1530;border:1px solid #2a4a8a;border-left:4px solid #00e5ff;border-radius:10px;padding:16px;margin:8px 0}
.mail .meta{color:#8fb0e0;font-size:.9rem}.mail h4{margin:6px 0}
.mail .btn{display:inline-block;background:#1a73e8;color:#fff;padding:8px 16px;border-radius:6px;margin-top:8px}
.ok{border-left-color:#00e676;background:#0b2a1c}
.bad{border-left-color:#ff1744;background:#2a0b14;animation:glitch .7s}
@keyframes glitch{0%,100%{transform:translate(0)}10%{transform:translate(-6px,2px);filter:hue-rotate(90deg)}30%{transform:translate(6px,-2px)}50%{transform:translate(-4px,0);filter:hue-rotate(-90deg)}70%{transform:translate(3px,2px)}}
.url{font-family:monospace;background:#050a18;border:1px dashed #00e5ff;padding:10px;border-radius:8px;word-break:break-all}
.dom{background:#ffea0033;color:#ffea00;border-radius:4px;padding:0 3px;font-weight:700;box-shadow:0 0 8px #ffea0066}
.dim{color:#7f8aa8}.strike{color:#ff6b81;text-decoration:line-through}
.badge{display:inline-block;margin:4px;padding:8px 12px;border-radius:20px;border:1px solid #00e5ff;background:#0d1530}
.badge.off{opacity:.3;border-color:#555}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def load_emails():
    try:
        return json.loads((Path(__file__).parent / "emails.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        return str(err)


EMAILS = load_emails()
if isinstance(EMAILS, str):
    st.error(f"Could not load emails.json: {EMAILS}")
    st.stop()

for k, v in dict(screen="menu", level=1, unlocked={1}, lvl_scores={}, lives=3, streak=0, best=0, idx=0,
                 queue=[], log=[], flawless=set(), cleared=set(), run=0, res=None, deadline=0, last_pts=0).items():
    S.setdefault(k, v)
S.setdefault("timer", False)


def real_domain(host):
    parts = host.split(".")
    n = 3 if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_PART else 2
    return ".".join(parts[-n:])


def link_html(url):
    """Show the true destination with the registrable domain highlighted."""
    u = urlparse(url)
    host = u.hostname or ""
    real = real_domain(host)
    userinfo = u.netloc.rsplit("@", 1)[0] + "@" if "@" in u.netloc else ""
    sub = host[: len(host) - len(real)]
    out = f"<span class='dim'>{u.scheme}://</span>"
    if userinfo:
        out += f"<span class='strike'>{html.escape(userinfo)}</span>"
    out += f"<span class='dim'>{html.escape(sub)}</span><span class='dom'>{html.escape(real)}</span><span class='dim'>{html.escape(u.path)}</span>"
    note = "<br><small>⚠ Everything before '@' is ignored by your browser.</small>" if userinfo else ""
    return f"<div class='url'>{out}</div><small>🎯 Real destination domain: <b>{html.escape(real)}</b>. Only the highlighted part decides where you land.</small>{note}"


def total_score():
    return sum(S.lvl_scores.values())


def mult():
    return min(1 + 0.25 * S.streak, 2.0)


def start_level(n):
    qs = [e for e in EMAILS if e["level"] == n]
    random.shuffle(qs)
    S.update(level=n, queue=qs, idx=0, lives=3, streak=0, screen="play", run=S.run + 1, res=None)
    S.lvl_scores[n] = 0
    S.log = [r for r in S.log if r["level"] != n]
    S.deadline = time.time() + TIME


def resolve(choice):
    e = S.queue[S.idx]
    chosen = {p for p in PARTS if S.get(f"fl_{S.run}_{S.idx}_{p}")} if choice else set()
    truth = set(e["flags"])
    found, missed, wrong = chosen & truth, truth - chosen, chosen - truth
    correct = choice == e["answer"]
    m = mult()
    if correct:
        pts = round(10 * m)
        S.streak += 1
        S.best = max(S.best, S.streak)
    else:
        pts = -5
        S.lives -= 1
        S.streak = 0
    fp = 5 * len(found) - 2 * len(wrong)
    perfect = bool(truth) and not missed and not wrong and e["answer"] == "phishing"
    if perfect:
        fp += 10
    S.lvl_scores[S.level] = S.lvl_scores.get(S.level, 0) + pts + fp
    S.last_pts = pts + fp
    previewed = bool(S.get(f"pv_{S.run}_{S.idx}"))
    S.log.append(dict(level=S.level, cat=e["cat"], correct=correct, found=len(found), truth=len(truth),
                      wrong=len(wrong), perfect=perfect, preview=previewed, answer=e["answer"], timeout=choice is None))
    S.res = dict(e=e, choice=choice, correct=correct, pts=pts, fp=fp, found=found, missed=missed, wrong=wrong, perfect=perfect, mult=m)
    S.screen = "feedback"


def hud():
    hearts = "❤️" * S.lives + "🖤" * (3 - S.lives)
    pop = "pop" if S.res else ""
    st.markdown(f"""<div class='hud'>
    <div class='box'><small>SCORE</small><b class='{pop}'>{total_score()}</b></div>
    <div class='box'><small>LIVES</small><b>{hearts}</b></div>
    <div class='box'><small>STREAK 🔥</small><b>{S.streak}</b></div>
    <div class='box'><small>MULTIPLIER</small><b>x{mult():.2f}</b></div></div>""", unsafe_allow_html=True)


@st.fragment(run_every=1)
def countdown():
    left = int(S.deadline - time.time())
    if left <= 0:
        st.rerun()
    st.progress(max(0, left) / TIME, text=f"⏱️ {left}s left")


def menu():
    st.markdown("<div class='title'>🛡️ PHISHGUARD</div>", unsafe_allow_html=True)
    st.caption("OSHC Cyber Defence Academy · Protecting international students from phishing")
    with st.expander("📖 How to play", expanded=True):
        st.markdown("1. Read each email. Flag the parts that look suspicious (+5 each, -2 for a wrong flag, +10 for a perfect sweep).\n"
                    "2. Use **🔍 Preview link** to see the real destination domain.\n"
                    "3. Choose **Report Phishing** or **Mark Safe** (+10 x streak multiplier, wrong = -5 and a life).\n"
                    "4. Reach the score target to unlock the next level.")
    st.toggle(f"⏱️ Timer mode ({TIME}s per email)", key="timer")
    for n, (name, story, need) in LEVELS.items():
        ok = n in S.unlocked
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"**Level {n}: {name}** {'✅' if n in S.cleared else '' if ok else '🔒'}  \n<small>{story} Target: {need} pts</small>", unsafe_allow_html=True)
        if c2.button("Play", key=f"lv{n}", disabled=not ok, width="stretch"):
            start_level(n)
            st.rerun()


def play():
    e = S.queue[S.idx]
    if S.timer and time.time() > S.deadline:
        resolve(None)
        st.rerun()
    hud()
    st.caption(f"Level {S.level}: {LEVELS[S.level][0]} · Email {S.idx + 1}/{len(S.queue)}")
    if S.timer:
        countdown()
    h = html.escape
    st.markdown(f"""<div class='mail'><div class='meta'>From: <b>{h(e['name'])}</b> &lt;{h(e['email'])}&gt;</div>
    <h4>{h(e['subject'])}</h4><p>{h(e['greeting'])},<br><br>{h(e['body'])}</p><span class='btn'>{h(e['link_text'])}</span></div>""", unsafe_allow_html=True)
    st.markdown("**🚩 Inspect: tick anything suspicious**")
    labels = {"sender": f"Sender address ({e['email']})", "greeting": f"Greeting (\"{e['greeting']}\")",
              "body": "Message wording / demands", "link": f"The link button (\"{e['link_text']}\")"}
    for p in PARTS:
        st.checkbox(labels[p], key=f"fl_{S.run}_{S.idx}_{p}")
    if st.toggle("🔍 Preview link (hover without clicking)", key=f"pv_{S.run}_{S.idx}"):
        st.markdown(link_html(e["url"]), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🎣 Report Phishing", width="stretch", type="primary"):
        resolve("phishing")
        st.rerun()
    if c2.button("✅ Mark Safe", width="stretch"):
        resolve("legit")
        st.rerun()


def feedback():
    r, e = S.res, S.res["e"]
    hud()
    if r["choice"] is None:
        head, cls = "⏱️ TIME'S UP", "bad"
    else:
        head, cls = ("✅ CORRECT", "ok") if r["correct"] else ("❌ WRONG", "bad")
    kind = "PHISHING" if e["answer"] == "phishing" else "LEGITIMATE"
    st.markdown(f"<div class='mail {cls}'><h3>{head}</h3>This email was <b>{kind}</b>.<br>"
                f"Classification {r['pts']:+d} (x{r['mult']:.2f}) · Flags {r['fp']:+d}"
                f"{' · 🔬 Perfect inspection +10' if r['perfect'] else ''}</div>", unsafe_allow_html=True)
    if e["flags"]:
        st.markdown("**Red flags in this email**")
        for p, why in e["flags"].items():
            icon = "🟢 Found" if p in r["found"] else "🔴 Missed"
            st.markdown(f"- {icon} · **{p.title()}**: {why}")
    else:
        st.markdown(f"**Why it's safe:** {e['why']}")
    if r["wrong"]:
        st.warning("False flags: " + ", ".join(p.title() for p in r["wrong"]))
    st.info(f"💡 {e['tip']}")
    st.code(e["url"], language=None)
    if st.button("Next ▶", type="primary", width="stretch"):
        S.idx += 1
        S.res = None
        S.deadline = time.time() + TIME
        S.screen = "gameover" if S.lives <= 0 else "level_end" if S.idx >= len(S.queue) else "play"
        st.rerun()


def gameover():
    st.markdown("<div class='mail bad'><h2>💀 SYSTEM COMPROMISED</h2>You ran out of lives. Scammers got in.</div>", unsafe_allow_html=True)
    st.metric("Level score", S.lvl_scores.get(S.level, 0))
    c1, c2 = st.columns(2)
    if c1.button("🔁 Retry level", width="stretch"):
        start_level(S.level)
        st.rerun()
    if c2.button("🏠 Menu", width="stretch"):
        S.screen = "menu"
        st.rerun()


def level_end():
    n, sc, need = S.level, S.lvl_scores.get(S.level, 0), LEVELS[S.level][2]
    passed = sc >= need
    st.markdown(f"<div class='title'>LEVEL {n} {'CLEARED' if passed else 'FAILED'}</div>", unsafe_allow_html=True)
    st.metric("Level score", sc, delta=f"target {need}", delta_color="off")
    st.progress(min(1.0, max(0, sc) / need))
    if S.lives == 3:
        S.flawless.add(n)
        st.success("💎 Flawless: no lives lost!")
    if passed:
        S.cleared.add(n)
        if n < 3:
            S.unlocked.add(n + 1)
            st.success(f"🔓 Level {n + 1} unlocked!")
    else:
        st.error("Not enough points. Spot more red flags to boost your score.")
    c1, c2 = st.columns(2)
    if passed and n < 3 and c1.button("Next level ▶", type="primary", width="stretch"):
        start_level(n + 1)
        st.rerun()
    if passed and n == 3 and c1.button("📊 Final report", type="primary", width="stretch"):
        S.screen = "report"
        st.rerun()
    if not passed and c1.button("🔁 Retry", width="stretch"):
        start_level(n)
        st.rerun()
    if c2.button("🏠 Menu", width="stretch"):
        S.screen = "menu"
        st.rerun()


def report():
    log = S.log
    n = max(1, len(log))
    acc = 100 * sum(r["correct"] for r in log) / n
    tr = sum(r["truth"] for r in log)
    fr = 100 * sum(r["found"] for r in log) / tr if tr else 0
    sec = max(0, min(100, round(0.6 * acc + 0.4 * fr - 3 * sum(r["wrong"] for r in log))))
    st.markdown("<div class='title'>📊 REPORT CARD</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(mode="gauge+number", value=sec, title={"text": "Security Score"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#00e5ff"},
               "steps": [{"range": [0, 50], "color": "#5c1020"}, {"range": [50, 80], "color": "#5c4a10"}, {"range": [80, 100], "color": "#0b3a24"}]}))
    fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=60, b=0))
    st.plotly_chart(fig, width="stretch")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total score", total_score())
    c2.metric("Accuracy", f"{acc:.0f}%")
    c3.metric("Best streak", S.best)
    cats = {}
    for r in log:
        a = cats.setdefault(r["cat"], [0, 0])
        a[0] += r["correct"]
        a[1] += 1
    pct = {CATS[k]: 100 * v[0] / v[1] for k, v in cats.items()}
    bar = go.Figure(go.Bar(x=list(pct.values()), y=list(pct.keys()), orientation="h",
                           marker_color=["#00e676" if v >= 80 else "#ffc400" if v >= 50 else "#ff1744" for v in pct.values()]))
    bar.update_layout(template="plotly_dark", title="Accuracy by category (%)", height=320, xaxis=dict(range=[0, 100]), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(bar, width="stretch")
    weak = min(pct, key=pct.get)
    st.warning(f"🎯 Weakest area: **{weak}** ({pct[weak]:.0f}%). Review those red flags before opening your next OSHC email.")
    ph = sum(r["correct"] and r["answer"] == "phishing" for r in log)
    dd = sum(r["preview"] and r["correct"] for r in log)
    badges = [("🎣 Phish Hunter", ph >= 5, "Reported 5+ phishing emails"), ("🔥 Streak Master", S.best >= 5, "Streak of 5"),
              ("🕵️ Domain Detective", dd >= 3, "Used Preview link on 3+ correct answers"),
              ("🔬 Perfect Inspector", any(r["perfect"] for r in log), "Found every red flag in an email"),
              ("💎 Flawless", bool(S.flawless), "Cleared a level without losing a life"),
              ("🏥 OSHC Guardian", len(S.cleared) == 3, "Cleared all 3 levels")]
    st.markdown("### 🏅 Badges")
    st.markdown("".join(f"<span class='badge {'' if ok else 'off'}' title='{d}'>{b}</span>" for b, ok, d in badges), unsafe_allow_html=True)
    if st.button("🏠 Back to menu", width="stretch"):
        S.screen = "menu"
        st.rerun()


{"menu": menu, "play": play, "feedback": feedback, "gameover": gameover, "level_end": level_end, "report": report}[S.screen]()
