
import streamlit as st
import speech_recognition as sr
import io
import re
import base64
from pathlib import Path


# ADVANCED VISHING AWARENESS GAME


BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"




# SOUND EFFECTS


SOUNDS_DIR = BASE_DIR.parent / "static" / "sounds"

def play_sound(filename):

    sound_file = SOUNDS_DIR / filename

    if not sound_file.exists():
        st.error(f"Sound not found: {sound_file}")
        return

    st.audio(
        sound_file.read_bytes(),
        format="audio/mpeg",
        autoplay=True
    )


# SCENARIOS — 4 × 10 = 40 POINTS


SCENARIOS = {
    1: {
        "name": "OTP Verification Scam",
        "audio": "advanced_call1.mp3",
        "opening": (
            "Hello, this is Daniel from Medibank OSHC. "
            "We detected suspicious activity on your account. "
            "Please tell me your six-digit verification code."
        ),
    },

    2: {
        "name": "Remote Access Scam",
        "audio": "advanced_call2.mp3",
        "opening": (
            "Hi there! How are you doing today? "
            "My name is Helena, and I'm calling from the "
            "Medibank Customer Service team. "
            "I hope you're having a lovely day! "

            "I'm following up regarding a security concern "
            "with your Medibank OSHC account. "
            "We've noticed some unusual activity, and we want "
            "to make sure your personal information is safe. "

            "To help secure your account, I'd like you to install "
            "a remote support application so I can check your device. "
            "Once you've installed it, please let me know."
        ),
    },

    3: {
        "name": "Banking Details Scam",
        "audio": "advanced_call3.mp3",
        "opening": (
            "Hi there! How are you doing today? "
            "My name is Olivia, and I'm calling from the "
            "Medibank OSHC Customer Service team. "
            "I hope you're having a good day! "

            "I'm calling regarding a small issue we've noticed "
            "with your recent OSHC insurance payment. "
            "It looks like your payment verification hasn't "
            "been completed successfully. "

            "To help resolve this, we need to verify your "
            "payment information. Could you please provide "
            "your card details so we can update your account? "

            "We'd like to get this sorted out today to avoid "
            "any interruption to your insurance coverage."
        ),
    },

    4: {
        "name": "Visa Cancellation Scam",
        "audio": "advanced_call4.mp3",
        "opening": (
            "Hello, this is an officer from the Australian "
            "Department of Home Affairs. There is an urgent "
            "issue with your student visa. Your visa may be "
            "cancelled unless you verify your identity. "
            "Please provide your passport number and visa details."

        ),
    },
}


# CALLER REACTIONS


REACTIONS = {
    "safe": (
        "I understand you're being careful, but this is urgent. "
        "We still need to resolve your account issue."
    ),
    "unsafe": (
        "Thank you for cooperating. There is one more "
        "security check we need to complete."
    ),
    "uncertain": (
        "I understand your concern, but we need to "
        "complete this process as soon as possible."
    ),
}


# SESSION STATE


defaults = {
    "game_stage": "incoming",
    "game_round": 1,
    "game_score": 0,
    "game_history": [],
    "previous_result": None,
    "current_feedback": None,
    "adv_record_version": 0,
    "adv_retry_required": False,
    "advanced_completed": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# IMPROVED RESPONSE EVALUATION


def evaluate_response(answer, round_no):

    text = answer.lower().replace("’", "'")
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return "uncertain"

    def matches(patterns):
        return any(
            re.search(pattern, text)
            for pattern in patterns
        )

 
    # Recognise safe refusals
    

    refusal_patterns = [
        r"\b(?:no|nope|nah|never)\b",
        r"\bno thanks\b",
        r"\bno thank you\b",
        r"\bi (?:can't|cannot|won't|wouldn't|will not|"
        r"would not|don't|do not)\b",
        r"\bi(?:'m| am) not\b",
        r"\bnot (?:sharing|giving|providing|installing|"
        r"downloading|allowing)\b",
        r"\brefuse\b",
        r"\bnot comfortable\b",
        r"\buncomfortable\b",
        r"\bnot interested\b",
        r"\bdon't trust\b",
        r"\bdo not trust\b",
        r"\bnot safe\b",
        r"\bthat's private\b",
        r"\bthat is private\b",
        r"\bcan't do that\b",
        r"\bwon't do that\b",
    ]

   
    # Recognise independent verification
    

    verification_patterns = [
        r"\b(?:call|contact|phone)\b.*"
        r"\b(?:medibank|bank|insurance|home affairs|"
        r"department|official)\b",

        r"\b(?:verify|check|confirm)\b.*"
        r"\b(?:myself|independently|official|website|directly)\b",

        r"\bi'll verify it myself\b",
        r"\bi will verify it myself\b",
        r"\bi'll call back\b",
        r"\bi will call back\b",
        r"\bhang up\b",
        r"\bend (?:this|the) call\b",
        r"\bofficial website\b",
    ]

   
    # Recognise unsafe agreement
   

    agreement_patterns = [
        r"\b(?:i'll|i will|i can|let me|i'm going to|"
        r"i am going to)\s+"
        r"(?:share|give|provide|tell|send|install|"
        r"download|allow|grant)\b",

        r"\b(?:sure|okay|ok|yes|yeah|yep)\b.*"
        r"\b(?:share|give|provide|send|install|"
        r"download|allow|grant)\b",

        r"\bi agree to\b",
        r"\bi'll do that\b",
        r"\bi will do that\b",
        r"\bgo ahead\b",
    ]

   
    # Recognise direct disclosure
  

    disclosure_patterns = [
        r"\b(?:my|the)\s+(?:otp|verification code|"
        r"password|pin|passport number|card number|"
        r"cvv)\s+is\b",

        r"\bhere(?:'s| is) my\b.*"
        r"\b(?:code|passport|card|password)\b",
    ]

    refusal = matches(refusal_patterns)
    verification = matches(verification_patterns)
    agreement = matches(agreement_patterns)
    disclosure = matches(disclosure_patterns)

   
    # Handle tricky / contradictory answers
    

    if re.search(
        r"\b(?:don't|do not)\s+mind\s+"
        r"(?:sharing|giving|providing|installing|downloading)\b",
        text,
    ):
        return "unsafe"

    if re.search(
        r"\b(?:can't|cannot|won't)\s+refuse\b",
        text,
    ):
        return "uncertain"

    if refusal and agreement:
        return "uncertain"

    if disclosure:
        return "unsafe"

    if agreement:
        return "unsafe"

    # Safe responses
    #

    if verification:
        return "safe"

    if refusal:
        return "safe"

    return "uncertain"



# SPEECH RECOGNITION


def recognise_voice(audio):

    recognizer = sr.Recognizer()

    with sr.AudioFile(io.BytesIO(audio.getvalue())) as source:
        recorded_audio = recognizer.record(source)

    return recognizer.recognize_google(
        recorded_audio,
        language="en-AU",
    )



# PLAY CALL AUDIO


def play_audio(filename):

    path = AUDIO_DIR / filename

    if path.exists():
        st.audio(str(path), format="audio/mpeg")
    else:
        st.caption(f"Audio not added yet: {filename}")





# DISPLAY RESPONSE FEEDBACK



def show_feedback(result, play_effect=False):

    if result == "safe":
        if play_effect:
            play_sound("correct.mp3")

        st.success("✅ Safe response! +10 points")
        st.write(
            "Excellent! You recognised the suspicious request "
            "and protected your sensitive information."
        )

    elif result == "unsafe":
        if play_effect:
            play_sound("incorrect.mp3")

        st.error("❌ Unsafe response! 0 points")
        st.write(
            "Do not share sensitive information or follow "
            "instructions from an unverified caller."
        )

    else:
        if play_effect:
            play_sound("incorrect.mp3")

        st.warning("🤔 Response needs review. 0 points")
        st.write(
            "Your answer was not clearly classified as safe. "
            "Refuse suspicious requests or verify the caller "
            "through an official channel."
        )




# RESET GAME


def reset_game():

    st.session_state.game_stage = "incoming"
    st.session_state.game_round = 1
    st.session_state.game_score = 0
    st.session_state.game_history = []
    st.session_state.previous_result = None
    st.session_state.current_feedback = None

    st.session_state.adv_record_version += 1
    st.session_state.adv_retry_required = False
    st.session_state.advanced_completed = False



# GAME INTERFACE

st.title("🎤 Advanced Vishing Game")

st.caption("Interactive Voice Phishing Awareness Simulation")

st.info("Educational simulation — not a real Medibank call.")

stage = st.session_state.game_stage



# INCOMING CALL


if stage == "incoming":

    st.subheader("📲 Incoming Call...")

    
    # Hidden ringing sound
    ring_file = SOUNDS_DIR / "ringing.mp3"

    if ring_file.exists():
        ring_base64 = base64.b64encode(
            ring_file.read_bytes()
        ).decode("utf-8")

        st.markdown(
            f"""
            <audio autoplay loop style="display:none;">
                <source
                    src="data:audio/mpeg;base64,{ring_base64}"
                    type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )


    st.write("📞 Medibank OSHC Support")
    st.caption("Unknown / Unverified Caller")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "📞 Answer Call",
            use_container_width=True
        ):
            st.session_state.game_stage = "conversation"
            st.rerun()

    with col2:
        if st.button(
            "❌ Decline Call",
            use_container_width=True
        ):
            st.session_state.game_stage = "declined"
            st.rerun()

    

# CONVERSATION SCREEN


elif stage == "conversation":

    round_no = st.session_state.game_round
    scenario = SCENARIOS[round_no]

    st.progress((round_no - 1) / 4)

    st.subheader(f"📞 Round {round_no} of 4")

    st.write(f"**Scenario: {scenario['name']}**")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Overall Score",
            f"{st.session_state.game_score}/40",
        )

    with col2:
        st.metric("Current Round", f"{round_no}/4")

    # Caller reacts to the previous round
    previous = st.session_state.previous_result

    if previous is not None:

        st.write("📞 Caller responds:")
        st.info(REACTIONS[previous])

        reaction_file = f"advanced_{previous}.mp3"
        play_audio(reaction_file)

    # Current scam call
    st.write("🔊 Caller continues:")

    st.warning(scenario["opening"])

    play_audio(scenario["audio"])

    st.write("🎤 Your turn. Speak to the caller.")

   
    # MICROPHONE RECORDING
    

    audio = st.audio_input(
        "Record Your Response",
        key=(
            f"record_round_{round_no}_"
            f"{st.session_state.adv_record_version}"
        ),
    )

    if (
        audio is not None
        and not st.session_state.adv_retry_required
    ):

        st.success("Voice recorded successfully!")
        st.audio(audio)

        if st.button(
            "🧠 Analyse My Response",
            key=f"analyse_round_{round_no}",
        ):

            try:

                with st.spinner("Understanding your answer..."):
                    answer = recognise_voice(audio)

                result = evaluate_response(answer, round_no)

                # Save history once
                st.session_state.game_history.append({
                    "round": round_no,
                    "scenario": scenario["name"],
                    "caller": scenario["opening"],
                    "answer": answer,
                    "result": result,
                })

                # Award points once per scenario
                if result == "safe":
                    st.session_state.game_score += 10

                st.session_state.previous_result = result

                st.session_state.current_feedback = {
                    "answer": answer,
                    "result": result,
                }

                st.session_state.adv_retry_required = False
                st.session_state.game_stage = "feedback"

                st.rerun()

            except sr.UnknownValueError:

                st.session_state.adv_retry_required = True
                st.rerun()

            except sr.RequestError:

                st.error(
                    "Speech recognition is unavailable. "
                    "Please check your internet connection."
                )

            except Exception as e:

                st.error(f"Voice processing error: {e}")

  
    # TRY AGAIN IF SPEECH IS NOT UNDERSTOOD
    

    if st.session_state.adv_retry_required:

        st.error(
            "❌ Could not understand your voice. "
            "Please try again."
        )

        if st.button(
            "🔄 Try Again",
            key=f"adv_retry_{round_no}",
        ):

            st.session_state.adv_record_version += 1
            st.session_state.adv_retry_required = False

            st.rerun()



# FEEDBACK SCREEN


elif stage == "feedback":

    round_no = st.session_state.game_round
    feedback = st.session_state.current_feedback

    st.subheader("📝 Your Spoken Response")

    st.write(feedback["answer"])

    show_feedback(feedback["result"], play_effect=True)

    st.metric(
        "Current Advanced Score",
        f"{st.session_state.game_score}/40",
    )

    if round_no < 4:

        if st.button("➡️ Continue Call"):

            st.session_state.game_round += 1

            st.session_state.adv_record_version += 1
            st.session_state.adv_retry_required = False

            st.session_state.game_stage = "conversation"

            st.rerun()

    else:

        st.success(
            "🎉 You have completed all four Advanced scenarios!"
        )

        if st.button("🏆 View Advanced Results"):

            st.session_state.advanced_completed = True
            st.session_state.game_stage = "results"

            st.rerun()



# ADVANCED COMPLETION SCREEN


elif stage == "results":

    st.session_state.advanced_completed = True

    st.title("🏆 Advanced Level Completed!")

    st.success(
        "🎉 Congratulations! You have completed all four scenarios!"
    )

    st.progress(1.0)

    final_score = st.session_state.game_score

    st.metric("Final Score", f"{final_score}/40")

    if final_score == 40:

        st.write("🌟 Perfect score! Excellent scam awareness!")

    elif final_score >= 20:

        st.write(
            "👏 Good job! Keep improving your scam awareness skills!"
        )

    else:

        st.write(
            "💡 Keep practising! Review the warning signs and try again."
        )

   
    # CONVERSATION HISTORY

    st.subheader("📜 Conversation History")

    for item in st.session_state.game_history:

        with st.expander(
            f"Round {item['round']}: {item['scenario']}"
        ):

            st.write("**Caller:**")
            st.write(item["caller"])

            st.write("**You:**")
            st.write(item["answer"])

            show_feedback(item["result"])

    st.caption(
        "Rule-based scoring may misclassify natural speech. "
        "Results are for educational use."
    )

    
    # PLAY AGAIN / MAIN MENU
    

    if st.button("🔄 Play Advanced Again"):

        reset_game()
        st.rerun()

    if st.button("🏠 Back to Main Menu"):

        st.switch_page("home.py")



# DECLINED CALL SCREEN


elif stage == "declined":

    st.success("✅ You declined the unknown call.")

    st.write(
        "Declining an unexpected call can be a safe choice. "
        "Verify account concerns through official channels."
    )

    if st.button("🔄 Start Simulation"):

        reset_game()
        st.rerun()

    if st.button("🏠 Back to Main Menu"):

        st.switch_page("home.py")
