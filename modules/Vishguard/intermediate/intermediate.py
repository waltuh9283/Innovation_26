
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# INTERMEDIATE LEVEL SOUND EFFECTS

import base64

SOUNDS_DIR = BASE_DIR.parent / "static" / "sounds"

WELCOME_SOUND = SOUNDS_DIR / "intermediate_start.mp3"


def play_sound(filename):
    sound_file = SOUNDS_DIR / filename

    if sound_file.exists():
        st.audio(
            sound_file.read_bytes(),
            format="audio/mpeg",
            autoplay=True
        )
    else:
        st.warning(f"Sound file not found: {filename}")


# Hidden welcome voice
def play_welcome_voice():
    if not WELCOME_SOUND.exists():
        st.warning("Intermediate welcome voice not found.")
        return

    audio_base64 = base64.b64encode(
        WELCOME_SOUND.read_bytes()
    ).decode("utf-8")

    st.markdown(
        f"""
        <audio autoplay style="display:none;">
            <source
                src="data:audio/mpeg;base64,{audio_base64}"
                type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )


# INTERMEDIATE LEVEL — INITIAL SESSION STATE


if "intermediate_scenario" not in st.session_state:
    st.session_state.intermediate_scenario = 1

if "intermediate_score" not in st.session_state:
    st.session_state.intermediate_score = 0

if "intermediate_completed" not in st.session_state:
    st.session_state.intermediate_completed = False



# SCENARIO DATA


scenarios = [
    {
        "title": "Fake OSHC Refund Call",
        "audio": "scenario1.mp3",
        "correct": 0,
        "explanation": (
            "🚨 This is a vishing attack. The caller promises an "
            "unexpected insurance refund, sends a suspicious link, "
            "and asks for sensitive banking information. "
            "Never provide banking details through unexpected links. "
            "Always contact your insurer through official channels."
        )
    },
    {
        "title": "Fake Medibank Account Verification",
        "audio": "scenario2.mp3",
        "correct": 0,
        "explanation": (
            "🚨 This is a vishing attack. The caller pretends to "
            "represent Medibank, requests passport information, "
            "and threatens insurance suspension. "
            "These are warning signs of social engineering. "
            "Always verify unexpected requests independently."
        )
    },
    {
        "title": "OSHC Information Call",
        "audio": "scenario3.mp3",
        "correct": 1,
        "explanation": (
            "✅ This is a fictional non-phishing example. "
            "The caller provides general information without "
            "requesting sensitive personal details or payments. "
            "However, a caller's identity cannot be confirmed "
            "from the conversation alone."
        )
    },
    {
        "title": "OSHC Appointment Information",
        "audio": "scenario4.mp3",
        "correct": 1,
        "explanation": (
            "✅ This fictional conversation demonstrates safer "
            "communication. The caller provides general healthcare "
            "information, does not request sensitive details or "
            "payments, and directs the student to the official "
            "insurance website. Always verify unexpected callers."
        )
    }
]



# PAGE HEADER


st.title("🟡 Intermediate Level")

st.write(
    "Listen to realistic phone calls, identify manipulation "
    "techniques, and decide whether each call is vishing."
)

total_scenarios = len(scenarios)
current_scenario = st.session_state.intermediate_scenario


# Welcome voice for Scenario 1
if (
    current_scenario == 1
    and st.session_state.get("intermediate_answer1") is None
):
    play_welcome_voice()


st.progress(
    min((current_scenario - 1) / total_scenarios, 1.0)
)

st.metric(
    "Current Score",
    f"{st.session_state.intermediate_score}/40"
)



# SCENARIOS 1–4


if 1 <= current_scenario <= total_scenarios:

    scenario = scenarios[current_scenario - 1]

    st.subheader(
        f"📞 Scenario {current_scenario}: {scenario['title']}"
    )

    st.write("🎧 Listen carefully to the conversation.")

    # Play scenario audio
    audio_file = BASE_DIR / "audio" / scenario["audio"]

    if audio_file.exists():
        st.audio(str(audio_file))
    else:
        st.warning(
            f"Scenario {current_scenario} audio not found."
        )

    # Answer options
    options = [
        "🚨 Yes, this is a phishing (vishing) call",
        "✅ No, this is a legitimate insurance call"
    ]

    correct_answer = options[scenario["correct"]]

    # Unique session-state keys for each scenario
    answer_key = f"intermediate_answer{current_scenario}"
    radio_key = f"intermediate_radio{current_scenario}"
    submit_key = f"intermediate_submit{current_scenario}"
    next_key = f"intermediate_next{current_scenario}"

    if answer_key not in st.session_state:
        st.session_state[answer_key] = None

    submitted_answer = st.session_state[answer_key]
    is_submitted = submitted_answer is not None

    # Display question
    answer = st.radio(
        "❓ Is this a phishing (vishing) call or a legitimate call?",
        options,
        index=None,
        key=radio_key,
        disabled=is_submitted
    )

  
    # SUBMIT ANSWER
    

    if not is_submitted:

        if st.button("Submit Answer", key=submit_key):

            if answer is None:
                st.warning("⚠️ Please select an answer first.")

            else:
                # Save the answer permanently for this attempt
                st.session_state[answer_key] = answer

                # Add points only once for a correct answer
                if answer == correct_answer:
                    st.session_state.intermediate_score += 10

                st.rerun()

    # FEEDBACK AFTER SUBMISSION
   

    if is_submitted:

        is_correct = submitted_answer == correct_answer

        if is_correct:

            st.success("🎉 Correct! +10 Points")
            play_sound("correct.mp3")

            win_image = BASE_DIR / "images" / "win.png"

            if win_image.exists():
                st.image(str(win_image), width=350)

        else:

            st.error("❌ Incorrect! 0 Points")
            play_sound("incorrect.mp3")

            lose_image = BASE_DIR / "images" / "lose.png"

            if lose_image.exists():
                st.image(str(lose_image), width=350)

        # Educational explanation
        st.info(scenario["explanation"])


    
        # NEXT SCENARIO / VIEW RESULTS
        

        if current_scenario < total_scenarios:

            if st.button(
                "Next Scenario ➡️",
                key=next_key
            ):
                st.session_state.intermediate_scenario += 1
                st.rerun()

        else:

            if st.button(
                "View Intermediate Results 🏆",
                key="intermediate_finish4"
            ):
                st.session_state.intermediate_completed = True
                st.session_state.intermediate_scenario = 5
                st.rerun()



# INTERMEDIATE LEVEL COMPLETION


elif current_scenario == 5:

    st.session_state.intermediate_completed = True

    st.title("🏆 Intermediate Level Completed!")

    st.success(
        "🎉 Congratulations! You have completed all four scenarios!"
    )

    st.metric(
        "Final Score",
        f"{st.session_state.intermediate_score}/40"
    )

    if st.session_state.intermediate_score == 40:

        st.write(
            "🌟 Perfect score! Excellent scam awareness!"
        )

    elif st.session_state.intermediate_score >= 20:

        st.write(
            "👏 Good job! Keep improving your scam awareness skills!"
        )

    else:

        st.write(
            "💡 Keep learning! Review the warning signs "
            "and practise identifying suspicious calls."
        )

   
    # PLAY INTERMEDIATE AGAIN
   

    if st.button(
        "🔄 Play Intermediate Again",
        key="intermediate_play_again"
    ):

        st.session_state.intermediate_scenario = 1
        st.session_state.intermediate_score = 0
        st.session_state.intermediate_completed = False

        # Clear answers and radio selections
        for i in range(1, 5):
            st.session_state.pop(
                f"intermediate_answer{i}", None
            )

            st.session_state.pop(
                f"intermediate_radio{i}", None
            )

        st.rerun()

   
    # BACK TO MAIN MENU
   

    if st.button(
        "🏠 Back to Main Menu",
        key="intermediate_back_home"
    ):
        st.switch_page("home.py")
