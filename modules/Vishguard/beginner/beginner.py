
import streamlit as st
from pathlib import Path

# BEGINNER LEVEL — BASIC SETUP


BASE_DIR = Path(__file__).resolve().parent



# BEGINNER LEVEL WELCOME VOICE


import base64

SOUNDS_DIR = BASE_DIR.parent / "static" / "sounds"
WELCOME_SOUND = SOUNDS_DIR / "beginner_start.mp3"

if (
    WELCOME_SOUND.exists()
    and st.session_state.get("beginner_scenario", 1) == 1
    and st.session_state.get("beginner_answer1") is None
):
    audio_bytes = WELCOME_SOUND.read_bytes()
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

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




# BEGINNER LEVEL SOUND EFFECTS


SOUNDS_DIR = BASE_DIR.parent / "static" / "sounds"

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


if "beginner_scenario" not in st.session_state:
    st.session_state.beginner_scenario = 1

if "beginner_score" not in st.session_state:
    st.session_state.beginner_score = 0

if "beginner_completed" not in st.session_state:
    st.session_state.beginner_completed = False


# SCENARIO DATA


scenarios = [
    {
        "title": "Suspicious Medibank OSHC Call",
        "audio": "scenario1.mp3",
        "question": "❓ What type of vishing attack is this?",
        "options": [
            "Fake payment / bank security scam",
            "Government / visa-authority impersonation",
            "Technical-support scam"
        ],
        "correct": 0,
        "explanation": (
            "🚨 The caller creates urgency and asks for sensitive "
            "financial information. This is a fake payment or "
            "bank security scam. Never share financial information "
            "during unexpected phone calls."
        )
    },
    {
        "title": "Payment Verification Link",
        "audio": "scenario2.mp3",
        "question": "❓ What is the main warning sign in this call?",
        "options": [
            "The caller asks the student to visit a Medibank office",
            "The caller sends a link and pressures the student "
            "to enter personal/payment details",
            "The caller explains general information about OSHC"
        ],
        "correct": 1,
        "explanation": (
            "🚨 The caller sends an unexpected link and pressures "
            "the student to provide sensitive personal or payment "
            "information. Verify suspicious requests through "
            "official channels."
        )
    },
    {
        "title": "Fake Account Security Call",
        "audio": "scenario3.mp3",
        "question": "❓ What should you do in this situation?",
        "options": [
            "Install the application and give the caller the access code",
            "Give the caller the code because they know about your OSHC",
            "End the call and independently contact the insurer through an official channel"
        ],
        "correct": 2,
        "explanation": (
            "🚨 The caller attempts to gain remote access to the "
            "student's device. Never install remote-access software "
            "or share access codes because of an unexpected call. "
            "Verify security requests independently."
        )
    },
    {
        "title": "Fake Visa Verification Call",
        "audio": "scenario4.mp3",
        "question": (
            "❓ What should you do when the caller asks "
            "for your personal details?"
        ),
        "options": [
            "Provide your passport number and date of birth",
            "Give your OSHC policy information to avoid visa problems",
            "End the call and verify the request through an official channel"
        ],
        "correct": 2,
        "explanation": (
            "🚨 Scammers may impersonate government or insurance "
            "representatives and use threats about visa status "
            "to obtain passport numbers, dates of birth, and "
            "insurance information. Always verify independently."
        )
    }
]



# PAGE HEADER


st.title("🟢 Beginner Level")

st.write(
    "🎧 Listen carefully to each call and choose the correct answer."
)

total_scenarios = len(scenarios)
current_scenario = st.session_state.beginner_scenario

st.progress(
    min((current_scenario - 1) / total_scenarios, 1.0)
)

st.metric(
    "Current Score",
    f"{st.session_state.beginner_score}/40"
)



# SCENARIOS 1–4


if 1 <= current_scenario <= total_scenarios:

    scenario = scenarios[current_scenario - 1]

    st.subheader(
        f"📞 Scenario {current_scenario}: {scenario['title']}"
    )

    st.write("🎧 Listen carefully to the phone call.")

    # Play scenario audio
    audio_file = BASE_DIR / "audio" / scenario["audio"]

    if audio_file.exists():
        st.audio(str(audio_file))
    else:
        st.warning(
            f"Scenario {current_scenario} audio was not found."
        )

    # Unique session state keys
    answer_key = f"beginner_answer{current_scenario}"
    radio_key = f"beginner_radio{current_scenario}"
    submit_key = f"beginner_submit{current_scenario}"
    next_key = f"beginner_next{current_scenario}"

    if answer_key not in st.session_state:
        st.session_state[answer_key] = None

    submitted_answer = st.session_state[answer_key]
    is_submitted = submitted_answer is not None

    # Display question
    answer = st.radio(
        scenario["question"],
        scenario["options"],
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
                # Save answer and lock it
                st.session_state[answer_key] = answer

                correct_answer = scenario["options"][
                    scenario["correct"]
                ]

                # Add points only once
                if answer == correct_answer:
                    st.session_state.beginner_score += 10

                st.rerun()


    
    # FEEDBACK AFTER SUBMISSION
    

    if is_submitted:

        correct_answer = scenario["options"][
            scenario["correct"]
        ]

        is_correct = submitted_answer == correct_answer

        # Play sound only once per submitted answer
        sound_key = f"beginner_sound_{current_scenario}"

        if is_correct:

            st.success("🎉 Correct! +10 Points")

            if not st.session_state.get(sound_key, False):
                play_sound("correct.mp3")
                st.session_state[sound_key] = True

            # Show balloons once per correct scenario
            balloon_key = f"beginner_balloons_{current_scenario}"

            if not st.session_state.get(balloon_key, False):
                st.balloons()
                st.session_state[balloon_key] = True

            win_image = BASE_DIR / "images" / "win.png"

            if win_image.exists():
                st.image(str(win_image), width=350)

        else:

            st.error("❌ Incorrect! 0 Points")

            if not st.session_state.get(sound_key, False):
                play_sound("incorrect.mp3")
                st.session_state[sound_key] = True

            lose_image = BASE_DIR / "images" / "lose.png"

            if lose_image.exists():
                st.image(str(lose_image), width=350)

        # Educational explanation for both answers
        st.info(scenario["explanation"])

       
        # NEXT SCENARIO
       

        if current_scenario < total_scenarios:

            if st.button(
                "Next Scenario ➡️",
                key=next_key
            ):
                st.session_state.beginner_scenario += 1
                st.rerun()

        else:

            if st.button(
                "View Beginner Results 🏆",
                key="beginner_finish4"
            ):
                st.session_state.beginner_completed = True
                st.session_state.beginner_scenario = 5
                st.rerun()



# BEGINNER LEVEL COMPLETION



elif current_scenario == 5:

    st.session_state.beginner_completed = True

    # Show balloons only once when results are opened
    if not st.session_state.get("beginner_balloons_shown", False):
        st.balloons()
        st.session_state.beginner_balloons_shown = True

    st.title("🏆 Beginner Level Completed!")


    st.success(
        "🎉 Congratulations! You completed all four scenarios!"
    )

    st.metric(
        "Final Score",
        f"{st.session_state.beginner_score}/40"
    )

    if st.session_state.beginner_score == 40:

        st.write(
            "🌟 Perfect score! Excellent vishing awareness!"
        )

    elif st.session_state.beginner_score >= 20:

        st.write(
            "👏 Good job! Keep improving your scam detection skills!"
        )

    else:

        st.write(
            "💡 Keep learning! Review the warning signs "
            "and practise identifying suspicious calls."
        )


    # PLAY BEGINNER AGAIN


    if st.button(
        "🔄 Play Beginner Again",
        key="beginner_play_again"
    ):

        st.session_state.beginner_scenario = 1
        st.session_state.beginner_score = 0
        st.session_state.beginner_completed = False

        # Clear saved answers and radio selections
        for i in range(1, 5):

            st.session_state.pop(
                f"beginner_answer{i}", None
            )

            st.session_state.pop(
                f"beginner_radio{i}", None
            )

        st.rerun()


    # BACK TO MAIN MENU


    if st.button(
        "🏠 Back to Main Menu",
        key="beginner_back_home"
    ):
        st.switch_page("home.py")
