
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent

st.title("🟡 Intermediate Level")
st.write(
    "Listen to realistic phone calls, identify manipulation "
    "techniques, and choose the safest response."
)

if "intermediate_scenario" not in st.session_state:
    st.session_state.intermediate_scenario = 1

if "intermediate_score" not in st.session_state:
    st.session_state.intermediate_score = 0

st.progress(
    (st.session_state.intermediate_scenario - 1) / 4
)

st.metric(
    "Current Score",
    f"{st.session_state.intermediate_score}/40"
)



# SCENARIO 1 — FAKE OSHC REFUND CALL

if st.session_state.intermediate_scenario == 1:

    st.subheader("📞 Scenario 1: Fake OSHC Refund Call")
    st.write("🎧 Listen carefully to the conversation.")

    # Play the audio
    audio_file = BASE_DIR / "audio" / "scenario1.mp3"

    if audio_file.exists():
        st.audio(str(audio_file))
    else:
        st.warning("Scenario 1 audio not found.")

    # Answer choices
    options = [
        "🚨 Yes, this is a phishing (vishing) call",
        "✅ No, this is a legitimate insurance call"
    ]

    correct_answer = options[0]

    # Store the submitted answer
    if "intermediate_answer1" not in st.session_state:
        st.session_state.intermediate_answer1 = None

    # Question
    answer = st.radio(
        "❓ Is this a phishing (vishing) call or a legitimate call?",
        options,
        index=None,
        key="intermediate_radio1",
        disabled=st.session_state.intermediate_answer1 is not None
    )

    # Submit answer
    if st.session_state.intermediate_answer1 is None:

        if st.button("Submit Answer", key="intermediate_submit1"):

            if answer is None:
                st.warning("⚠️ Please select an answer first.")

            else:
                st.session_state.intermediate_answer1 = answer

                if answer == correct_answer:
                    st.session_state.intermediate_score += 10

                st.rerun()

    # Show feedback after submission
    if st.session_state.intermediate_answer1 is not None:

        if st.session_state.intermediate_answer1 == correct_answer:

            st.success("🎉 Correct! You identified the vishing attack!")

            win_image = BASE_DIR / "images" / "win.png"

            if win_image.exists():
                st.image(str(win_image), width=350)

            st.markdown("### 🏆 +15 Points")

        else:

            st.error("❌ Incorrect! This was a vishing attack.")

            lose_image = BASE_DIR / "images" / "lose.png"

            if lose_image.exists():
                st.image(str(lose_image), width=350)

        # Educational explanation
        st.info(
            "🚨 This is a vishing attack. The caller promises an "
            "unexpected insurance refund, sends a suspicious link, "
            "and asks for sensitive banking information. "
            "Never provide banking details through unexpected links. "
            "Always contact your insurer through official channels."
        )

        # Next scenario
        if st.button("Next Scenario ➡️", key="intermediate_next1"):
            st.session_state.intermediate_scenario = 2
            st.rerun()



# SCENARIO 2 — FAKE MEDIBANK ACCOUNT VERIFICATION

if st.session_state.intermediate_scenario == 2:

    st.subheader("📞 Scenario 2: Fake Medibank Account Verification")
    st.write("🎧 Listen carefully to the conversation.")

    # Play audio
    audio_file2 = BASE_DIR / "audio" / "scenario2.mp3"

    if audio_file2.exists():
        st.audio(str(audio_file2))
    else:
        st.warning("Scenario 2 audio not found.")

    # Answer choices
    options2 = [
        "🚨 Yes, this is a phishing (vishing) call",
        "✅ No, this is a legitimate insurance call"
    ]

    correct_answer2 = options2[0]

    # Store submitted answer
    if "intermediate_answer2" not in st.session_state:
        st.session_state.intermediate_answer2 = None

    answer2 = st.radio(
        "❓ Is this a phishing (vishing) call or a legitimate call?",
        options2,
        index=None,
        key="intermediate_radio2",
        disabled=st.session_state.intermediate_answer2 is not None
    )

    # Submit answer
    if st.session_state.intermediate_answer2 is None:

        if st.button("Submit Answer", key="intermediate_submit2"):

            if answer2 is None:
                st.warning("⚠️ Please select an answer first.")

            else:
                st.session_state.intermediate_answer2 = answer2

                if answer2 == correct_answer2:
                    st.session_state.intermediate_score += 10

                st.rerun()

    # Feedback
    if st.session_state.intermediate_answer2 is not None:

        if st.session_state.intermediate_answer2 == correct_answer2:

            st.success("🎉 Correct! You identified the vishing attack!")

            win_image2 = BASE_DIR / "images" / "win.png"

            if win_image2.exists():
                st.image(str(win_image2), width=350)

            st.markdown("### 🏆 +10 Points")

        else:

            st.error("❌ Incorrect! This was a vishing attack.")

            lose_image2 = BASE_DIR / "images" / "lose.png"

            if lose_image2.exists():
                st.image(str(lose_image2), width=350)

        # Educational feedback
        st.info(
            "🚨 Warning signs: The caller pretends to represent "
            "Medibank, requests sensitive passport information, "
            "and threatens insurance suspension. "
            "This is a fear-based social engineering technique. "
            "Always verify unexpected calls through official channels."
        )

        # Move to Scenario 3
        if st.button("Next Scenario ➡️", key="intermediate_next2"):
            st.session_state.intermediate_scenario = 3
            st.rerun()


# SCENARIO 3 — LEGITIMATE OSHC INFORMATION CALL

if st.session_state.intermediate_scenario == 3:

    st.subheader("📞 Scenario 3: OSHC Information Call")
    st.write("🎧 Listen carefully and decide whether this is a scam.")

    audio_file3 = BASE_DIR / "audio" / "scenario3.mp3"

    if audio_file3.exists():
        st.audio(str(audio_file3))
    else:
        st.warning("Scenario 3 audio not found.")

    options3 = [
        "🚨 Yes, this is a phishing (vishing) call",
        "✅ No, this is a legitimate insurance call"
    ]

    # Correct answer is NON-PHISHING
    correct_answer3 = options3[1]

    if "intermediate_answer3" not in st.session_state:
        st.session_state.intermediate_answer3 = None

    answer3 = st.radio(
        "❓ Is this a phishing (vishing) call or a legitimate call?",
        options3,
        index=None,
        key="intermediate_radio3",
        disabled=st.session_state.intermediate_answer3 is not None
    )

    if st.session_state.intermediate_answer3 is None:

        if st.button("Submit Answer", key="intermediate_submit3"):

            if answer3 is None:
                st.warning("⚠️ Please select an answer first.")

            else:
                st.session_state.intermediate_answer3 = answer3

                if answer3 == correct_answer3:
                    st.session_state.intermediate_score += 10

                st.rerun()

    if st.session_state.intermediate_answer3 is not None:

        if st.session_state.intermediate_answer3 == correct_answer3:

            st.success("🎉 Correct! This is a non-phishing example.")

            win_image3 = BASE_DIR / "images" / "win.png"

            if win_image3.exists():
                st.image(str(win_image3), width=350)

            st.markdown("### 🏆 +10 Points")

        else:

            st.error("❌ Incorrect! This is a non-phishing example.")

            lose_image3 = BASE_DIR / "images" / "lose.png"

            if lose_image3.exists():
                st.image(str(lose_image3), width=350)

        st.info(
            "✅ This fictional conversation demonstrates safer "
            "communication. The caller provides general information, "
            "does not request passwords, passport numbers, or "
            "banking details, and encourages the student to use "
            "the official insurance website. However, a caller's "
            "identity cannot be verified from the conversation alone."
        )

        if st.button("Next Scenario ➡️", key="intermediate_next3"):
            st.session_state.intermediate_scenario = 4
            st.rerun()


 
# SCENARIO 4 — OSHC APPOINTMENT INFORMATION CALL

if st.session_state.intermediate_scenario == 4:

    st.subheader("📞 Scenario 4: OSHC Appointment Information")
    st.write("🎧 Listen to the conversation and choose your answer.")

    # Play audio
    audio_file4 = BASE_DIR / "audio" / "scenario4.mp3"

    if audio_file4.exists():
        st.audio(str(audio_file4))
    else:
        st.warning("Scenario 4 audio not found.")

    # Answer options
    options4 = [
        "🚨 Yes, this is a phishing (vishing) call",
        "✅ No, this is a legitimate insurance call"
    ]

    # Correct answer: Non-phishing
    correct_answer4 = options4[1]

    # Store submitted answer
    if "intermediate_answer4" not in st.session_state:
        st.session_state.intermediate_answer4 = None

    answer4 = st.radio(
        "❓ Is this a phishing (vishing) call or a legitimate call?",
        options4,
        index=None,
        key="intermediate_radio4",
        disabled=st.session_state.intermediate_answer4 is not None
    )

    # Submit answer
    if st.session_state.intermediate_answer4 is None:

        if st.button("Submit Answer", key="intermediate_submit4"):

            if answer4 is None:
                st.warning("⚠️ Please select an answer first.")

            else:
                st.session_state.intermediate_answer4 = answer4

                if answer4 == correct_answer4:
                    st.session_state.intermediate_score += 10

                st.rerun()

    # Display feedback
    if st.session_state.intermediate_answer4 is not None:

        if st.session_state.intermediate_answer4 == correct_answer4:

            st.success("🎉 Correct! This is a non-phishing example.")

            win_image4 = BASE_DIR / "images" / "win.png"

            if win_image4.exists():
                st.image(str(win_image4), width=350)

            st.markdown("### 🏆 +10 Points")

        else:

            st.error("❌ Incorrect! This is a non-phishing example.")

            lose_image4 = BASE_DIR / "images" / "lose.png"

            if lose_image4.exists():
                st.image(str(lose_image4), width=350)

        # Educational feedback
        st.info(
            "✅ This fictional conversation demonstrates safer "
            "communication. The caller provides general healthcare "
            "information, does not request sensitive personal details "
            "or payments, and directs the student to the official "
            "insurance website. Remember that the caller's identity "
            "cannot be confirmed from the conversation alone."
        )

        # Finish Intermediate Level
        if st.button("Finish Intermediate Level 🏆", key="intermediate_finish4"):
            st.session_state.intermediate_scenario = 5
            st.rerun()


# INTERMEDIATE LEVEL COMPLETION

if st.session_state.intermediate_scenario == 5:

    st.balloons()

    st.title("🏆 Intermediate Level Completed!")

    st.success("🎉 Congratulations! You completed all four scenarios.")

    st.metric(
        "Your Final Score",
        f"{st.session_state.intermediate_score}/40"
    )

    if st.session_state.intermediate_score == 40:
        st.write("🌟 Perfect score! Excellent scam awareness!")
    elif st.session_state.intermediate_score >= 20:
        st.write("👏 Good job! Keep practising your scam detection skills.")
    else:
        st.write("💡 Keep learning! Review the warning signs and try again.")

    if st.button("🔄 Play Intermediate Again"):

        st.session_state.intermediate_scenario = 1
        st.session_state.intermediate_score = 0

        for i in range(1, 5):
            st.session_state.pop(f"intermediate_answer{i}", None)
            st.session_state.pop(f"intermediate_radio{i}", None)

        st.rerun()

    if st.button("🏠 Back to Main Menu"):
        st.switch_page("home.py")
