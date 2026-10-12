# Innovation_26
Python-based web application intended for international students to improve
their ability in cybersecurity awareness and their OSHC healthcare information. 

International students first moving to Australia are commonly unsure about the OSHC and healthcare, which may further impact their susceptibility to cybersecurity threats. 
Our team propose an interactive tool students can use early in their student journey or before they arrive, including three gamified exercises; spot the fake email, tell a real caller from an fake or AI voice, and information about what OSHC covers and why it matters, with little to no data collection. 
We intend to communicate the essentials, explained clearly and catered for Medibank international students with security and privacy as a fundamental design pillar.

Streamlit is used to present Python code as a web application.​

## How to run it
1. Install Python 3.10 or newer.
2. From the repo folder, run `python3 -m venv .venv`
3. Run `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows)
4. Run `pip install -r requirements.txt`
5. Run `streamlit run app.py`
6. Your browser opens the home page at http://localhost:8501

## Structure
- `app.py`: home page and router. Picks which module to show from `st.session_state.page`.
- `modules/phishing/`: PhishGuard (Streamlit), questions in `emails.json`.
- `modules/oshc/`: Medibank OSHC Basics, content in `oshc.json`.
- `modules/vishing/`: placeholder "coming soon" screen until the audio module is built.
- `ui/ui.py`: shared buttons, progress bar, feedback and results helpers.
- `assets/`: logo, pixel font, and (later) audio clips.

Each module has a `render()` function. To add a module: give it a `render()`, add its folder in `app.py`, and add it to `MODULES` and `PAGES`.
