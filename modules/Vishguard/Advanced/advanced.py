
import streamlit as st
import speech_recognition as sr
import io
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"

# Three different scam scenarios
SCENARIOS = {
    1: {
        "name": "OTP Verification Scam",
        "request": "share your verification code",
        "audio": "advanced_call1.mp3",
        "opening": (
            "Hello, this is Daniel from Medibank OSHC. "
            "We detected suspicious activity on your account. "
            "Please tell me your six-digit verification code."
        )
    },
    2: {
        "name": "Remote Access Scam",
        "request": "install remote support software",
        "audio": "advanced_remote.mp3",
        "opening": (
            "I understand your concern. To secure your account, "
            "please install the remote support application "
            "so I can check your device."
        )
    },
    3: {
        "name": "Banking Details Scam",
        "request": "provide your banking details",
        "audio": "advanced_bank.mp3",
        "opening": (
            "Your OSHC account may be suspended. "
            "To verify your payment information, "
            "please provide your card details."
        )
    }
}

# Different caller reactions to previous answers
REACTIONS = {
    "safe": (
        "I understand you're being careful, but this is "
        "urgent. We still need to resolve your account issue."
    ),
    "unsafe": (
        "Thank you for cooperating. There is one more "
        "security check we need to complete."
    ),
    "uncertain": (
        "I understand your questions, but we need to "
        "complete this process as soon as possible."
    )
}

defaults = {
    "game_stage": "incoming",
    "game_round": 1,
    "game_score": 0,
    "game_history": [],
    "previous_result": None,
    "current_feedback": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def has(pattern, text):
    return re.search(pattern, text) is not None


def evaluate_response(answer, round_no):
    text = answer.lower().replace("’", "'")
    text = re.sub(r"\s+", " ", text).strip()

    # Common refusal phrases
    refusal = (
        r"\b(?:i\s+)?(?:can't|cannot|won't|will not|"
        r"don't|do not|refuse to|wouldn't|would not)\s+"
        r"(?:share|give|provide|tell|send|install|"
        r"download|allow|do)\b"
    )

    # Positive agreement to unsafe requests
    agreement = (
        r"\b(?:i will|i'll|i can|let me|i am going to)\s+"
        r"(?:share|give|provide|tell|send|install|"
        r"download|allow)\b"
    )

    # Sharing secrets directly
    secrets = (
        r"\b(?:my|the)\s+(?:verification\s+)?"
        r"(?:code|password|pin)\s+is\b"
    )

    # Independent verification
    verify = (
        r"\b(?:call|contact|verify with)\s+"
        r"(?:medibank|the bank|the company|"
        r"official support)\b|"
        r"\b(?:hang up|end the call|official website)\b"
    )

    # Unsafe actions take priority
    if has(agreement, text) or has(secrets, text):
        # A refusal and an agreement in one answer
        # require review rather than automatic scoring
        if has(refusal, text):
            return "uncertain"
        return "unsafe"

    if has(verify, text):
        return "safe"

    if round_no == 1:
        # Refusing to provide OTP or verification code
        if has(refusal, text):
            return "safe"
        if has(r"\b(?:no|never)\b.*\b(?:code|otp|pin)\b", text):
            return "safe"

    elif round_no == 2:
        # Refusing software installation or remote access
        if has(refusal, text):
            return "safe"
        if has(r"\b(?:no|never)\b.*\b(?:install|download|access)\b", text):
            return "safe"

    elif round_no == 3:
        # Refusing to provide financial information
        if has(refusal, text):
            return "safe"
        if has(r"\b(?:no|never)\b.*\b(?:card|bank|payment)\b", text):
            return "safe"

    return "uncertain"


def recognise_voice(audio):
    recognizer = sr.Recognizer()

    with sr.AudioFile(io.BytesIO(audio.getvalue())) as source:
        recorded = recognizer.record(source)

    return recognizer.recognize_google(
        recorded, language="en-AU"
    )


def play_audio(filename):
    path = AUDIO_DIR / filename

    if path.exists():
        st.audio(str(path), format="audio/mpeg")
    else:
        st.caption(f"Audio not added yet: {filename}")


def show_feedback(result):
    if result == "safe":
        st.success("✅ Safe response! +5 points")
        st.write("You protected your sensitive information.")
    elif result == "unsafe":
        st.error("⚠️ Unsafe response! 0 points")
        st.write(
            "Never share sensitive information or "
            "grant remote access to an unverified caller."
        )
    else:
        st.warning("🤔 Response needs review. 0 points")
        st.write(
            "The response was not clearly classified. "
            "Try giving a more explicit refusal."
        )


def reset_game():
    st.session_state.game_stage = "incoming"
    st.session_state.game_round = 1
    st.session_state.game_score = 0
    st.session_state.game_history = []
    st.session_state.previous_result = None
    st.session_state.current_feedback = None


# GAME INTERFACE
st.title("🎤 Advanced Vishing Game")
st.caption("Interactive Voice Phishing Awareness Simulation")
st.info("Educational simulation — not a real Medibank call.")

stage = st.session_state.game_stage

if stage == "incoming":
    st.subheader("📲 Incoming Call...")
    st.write("📞 Medibank OSHC Support")
    st.caption("Unknown / Unverified Caller")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📞 Answer Call", use_container_width=True):
            st.session_state.game_stage = "conversation"
            st.rerun()

    with col2:
        if st.button("❌ Decline Call", use_container_width=True):
            st.session_state.game_stage = "declined"
            st.rerun()


elif stage == "conversation":
    round_no = st.session_state.game_round
    scenario = SCENARIOS[round_no]

    st.progress((round_no - 1) / 3)
    st.subheader(f"📞 Round {round_no} of 3")
    st.write(f"**Scenario: {scenario['name']}**")
    st.metric("Score", f"{st.session_state.game_score}/15")

    previous = st.session_state.previous_result

    # Caller reacts to the previous round
    if previous is not None:
        st.write("📞 Caller responds:")
        st.info(REACTIONS[previous])

        reaction_file = f"advanced_{previous}.mp3"
        play_audio(reaction_file)

    st.write("🔊 Caller continues:")
    st.warning(scenario["opening"])
    play_audio(scenario["audio"])

    st.write("🎤 Your turn. Speak to the caller.")

    audio = st.audio_input(
        "Record Your Response",
        key=f"record_round_{round_no}"
    )

    if audio is not None:
        st.success("Voice recorded successfully!")
        st.audio(audio)

        if st.button("🧠 Analyse My Response"):
            try:
                with st.spinner("Understanding your answer..."):
                    answer = recognise_voice(audio)

                result = evaluate_response(answer, round_no)

                st.session_state.game_history.append({
                    "round": round_no,
                    "scenario": scenario["name"],
                    "caller": scenario["opening"],
                    "answer": answer,
                    "result": result
                })

                if result == "safe":
                    st.session_state.game_score += 5

                st.session_state.previous_result = result
                st.session_state.current_feedback = {
                    "answer": answer,
                    "result": result
                }
                st.session_state.game_stage = "feedback"
                st.rerun()

            except sr.UnknownValueError:
                st.error("Could not understand your voice. Try again.")
            except sr.RequestError:
                st.error("Speech recognition service unavailable.")
            except Exception as e:
                st.error(f"Error: {e}")


elif stage == "feedback":
    feedback = st.session_state.current_feedback

    st.subheader("📝 Your Spoken Response")
    st.write(feedback["answer"])
    show_feedback(feedback["result"])

    if st.session_state.game_round < 3:
        if st.button("➡️ Continue Call"):
            st.session_state.game_round += 1
            st.session_state.game_stage = "conversation"
            st.rerun()
    else:
        if st.button("🏆 View Final Results"):
            st.session_state.game_stage = "results"
            st.rerun()


elif stage == "results":
    st.title("🏆 Simulation Complete!")
    st.progress(1.0)

    score = st.session_state.game_score
    st.metric("Final Score", f"{score}/15")

    if score == 15:
        st.success("Excellent cybersecurity awareness!")
    elif score >= 10:
        st.info("Good work! Review your weaker responses.")
    else:
        st.warning("More cybersecurity practice recommended.")

    st.subheader("📜 Conversation History")

    for item in st.session_state.game_history:
        with st.expander(
            f"Round {item['round']}: {item['scenario']}",
            expanded=True
        ):
            st.write("**Caller:**", item["caller"])
            st.write("**You:**", item["answer"])
            show_feedback(item["result"])

    st.caption(
        "Keyword-based prototype scoring may misclassify "
        "natural speech. Results are for educational use."
    )

    if st.button("🔄 Play Again"):
        reset_game()
        st.rerun()


elif stage == "declined":
    st.success("You declined the unknown call.")
    st.write(
        "This is a safe choice. Verify any account "
        "concerns through official contact channels."
    )

    if st.button("🔄 Try Again"):
        reset_game()
        st.rerun()
