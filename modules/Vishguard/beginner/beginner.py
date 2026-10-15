import streamlit as st
from pathlib import Path

@st.dialog("🏆 Beginner Level Complete!")
def completion_popup():
    st.balloons()

    st.success("🎉 Congratulations! You completed the Beginner Level!")

    st.metric(
        "Final Score",
        f"{st.session_state.beginner_score}/40"
    )

    st.write("🥷 Amazing work! You are becoming a Vishing Ninja!")

    if st.button("🎉 Continue", key="close_popup"):
        st.session_state.popup_seen = True
        st.rerun()

# -----------------------------------
# BASIC SETUP
# -----------------------------------

BASE_DIR = Path(__file__).parent

st.title("🟢 Beginner Level")
st.write("Listen carefully and identify the vishing attack.")

# Keep track of which scenario the player is on
if "beginner_scenario" not in st.session_state:
    st.session_state.beginner_scenario = 1

# Keep track of score
if "beginner_score" not in st.session_state:
    st.session_state.beginner_score = 0


# ===================================
# SCENARIO 1
# ===================================

if st.session_state.beginner_scenario == 1:

    st.subheader("📞 Scenario 1: Suspicious Medibank OSHC Call")

    st.write(
        "Listen carefully to the phone call and identify "
        "the type of vishing attack."
    )

    audio1 = BASE_DIR / "audio" / "scenario1.mp3"

    st.markdown("### 🎧 Listen to the call")

    if audio1.exists():
        st.audio(str(audio1))
    else:
        st.warning("Scenario 1 audio was not found.")

    answer1 = st.radio(
        "❓ What type of vishing attack is this?",
        [
            "Fake payment / bank security scam",
            "Government / visa-authority impersonation",
            "Technical-support scam"
        ],
        index=None,
        key="answer1",
        disabled=st.session_state.get("scenario1_correct", False)
    )

    if "scenario1_correct" not in st.session_state:
        st.session_state.scenario1_correct = False

    if not st.session_state.scenario1_correct:

        if st.button("Submit Answer", key="submit1"):

            if answer1 is None:

                st.warning("⚠️ Please select an answer first.")

            elif answer1 == "Fake payment / bank security scam":

                st.session_state.scenario1_correct = True
                st.session_state.beginner_score += 10
                st.rerun()

            else:

                st.error("❌ Incorrect — try again!")

                lose_image = BASE_DIR / "images" / "lose.png"

                if lose_image.exists():
                    st.image(str(lose_image), width=400)

                st.warning(
                    "Look for urgency, threats about your insurance "
                    "and requests for sensitive payment information."
                )

    else:

        st.success("🎉 Correct! You spotted the vishing attack!")
        st.balloons()

        win_image = BASE_DIR / "images" / "win.png"

        if win_image.exists():
            st.image(str(win_image), width=400)

        st.info(
            "The caller creates urgency and asks for sensitive "
            "financial information. This is a major warning sign."
        )

        st.markdown("## 🏆 Scenario 1 Complete!")
        st.metric("Current Score", f"{st.session_state.beginner_score}/40")

        if st.button("Next Scenario ➡️"):

            st.session_state.beginner_scenario = 2
            st.rerun()


# ===================================
# SCENARIO 2
# ===================================

elif st.session_state.beginner_scenario == 2:

    st.subheader("📞 Scenario 2: Payment Verification Link")

    st.write(
        "Listen carefully to the call and identify "
        "the main warning sign."
    )

    audio2 = BASE_DIR / "audio" / "scenario2.mp3"

    st.markdown("### 🎧 Listen to the call")

    if audio2.exists():
        st.audio(str(audio2))
    else:
        st.warning("Scenario 2 audio was not found.")

    answer2 = st.radio(
        "❓ What is the main warning sign in this call?",
        [
            "The caller asks the student to visit a Medibank office",
            "The caller sends a link and pressures the student "
            "to enter personal/payment details",
            "The caller explains general information about OSHC"
        ],
        index=None,
        key="answer2",
        disabled=st.session_state.get("scenario2_correct", False)
    )

    if "scenario2_correct" not in st.session_state:
        st.session_state.scenario2_correct = False

    if not st.session_state.scenario2_correct:

        if st.button("Submit Answer", key="submit2"):

            correct_answer = (
                "The caller sends a link and pressures the student "
                "to enter personal/payment details"
            )

            if answer2 is None:

                st.warning("⚠️ Please select an answer first.")

            elif answer2 == correct_answer:

                st.session_state.scenario2_correct = True
                st.session_state.beginner_score += 10
                st.rerun()

            else:

                st.error("❌ Incorrect — try again!")

                lose_image = BASE_DIR / "images" / "lose.png"

                if lose_image.exists():
                    st.image(str(lose_image), width=400)

                st.warning(
                    "An unexpected caller sending a link and "
                    "pressuring you to enter sensitive information "
                    "is a major warning sign."
                )

    else:

        st.success("🎉 Correct! You spotted the phishing/vishing attack!")
        st.balloons()

        win_image = BASE_DIR / "images" / "win.png"

        if win_image.exists():
            st.image(str(win_image), width=400)

        st.info(
            "Never trust an unexpected link just because someone "
            "sends it while speaking to you on the phone. "
            "Verify the request independently using an official channel."
        )

        st.markdown("## 🏆 Scenario 2 Complete!")
        st.metric("Current Score", f"{st.session_state.beginner_score}/40")

        if st.button("Next Scenario ➡️", key="next3"):
            st.session_state.beginner_scenario = 3
            st.rerun()

        # ===================================
# SCENARIO 3 - FAKE TECHNICAL SUPPORT
# ===================================

elif st.session_state.beginner_scenario == 3:

    st.subheader("📞 Scenario 3: Fake Account Security Call")

    st.write(
        "Listen to the call and choose the safest action."
    )

    audio3 = BASE_DIR / "audio" / "scenario3.mp3"

    st.markdown("### 🎧 Listen to the call")

    if audio3.exists():
        st.audio(str(audio3))
    else:
        st.warning("Scenario 3 audio was not found.")

    answer3 = st.radio(
        "❓ What should you do in this situation?",
        [
            "Install the application and give the caller the access code",
            "Give the caller the code because they know about your OSHC",
            "End the call and independently contact the insurer through an official channel"
        ],
        index=None,
        key="answer3",
        disabled=st.session_state.get("scenario3_correct", False)
    )

    if "scenario3_correct" not in st.session_state:
        st.session_state.scenario3_correct = False

    if not st.session_state.scenario3_correct:

        if st.button("Submit Answer", key="submit3"):

            if answer3 is None:
                st.warning("⚠️ Please select an answer first.")

            elif answer3 == (
                "End the call and independently contact the insurer through an official channel"
            ):
                st.session_state.scenario3_correct = True
                st.session_state.beginner_score += 10
                st.rerun()

            else:
                st.error("❌ Incorrect — try again!")

                lose_image = BASE_DIR / "images" / "lose.png"

                if lose_image.exists():
                    st.image(str(lose_image), width=400)

                st.warning(
                    "Never install remote-access software or share "
                    "access codes because of an unexpected phone call."
                )

    else:
        st.success("🎉 Correct! You identified the attack!")
        st.balloons()

        win_image = BASE_DIR / "images" / "win.png"

        if win_image.exists():
            st.image(str(win_image), width=400)

        st.info(
            "The caller tried to gain remote access to your device. "
            "Always verify unexpected security requests independently."
        )

        st.markdown("### 🏆 Scenario 3 Complete!")

        st.metric(
            "Current Score",
            f"{st.session_state.beginner_score}/40"
        )

        if st.button("Next Scenario ➡️", key="next4"):
            st.session_state.beginner_scenario = 4
            st.rerun()

# ===================================
# SCENARIO 4 - FAKE VISA VERIFICATION
# ===================================

elif st.session_state.beginner_scenario == 4:

    st.subheader("📞 Scenario 4: Fake Visa Verification Call")

    st.write(
        "Listen carefully to the call and identify "
        "the safest action."
    )

    audio4 = BASE_DIR / "audio" / "scenario4.mp3"

    st.markdown("### 🎧 Listen to the call")

    if audio4.exists():
        st.audio(str(audio4))
    else:
        st.warning("Scenario 4 audio was not found.")

    answer4 = st.radio(
        "❓ What should you do when the caller asks for your personal details?",
        [
            "Provide your passport number and date of birth",
            "Give your OSHC policy information to avoid visa problems",
            "End the call and verify the request through an official channel"
        ],
        index=None,
        key="answer4",
        disabled=st.session_state.get("scenario4_correct", False)
    )

    if "scenario4_correct" not in st.session_state:
        st.session_state.scenario4_correct = False

    if not st.session_state.scenario4_correct:

        if st.button("Submit Answer", key="submit4"):

            if answer4 is None:
                st.warning("⚠️ Please select an answer first.")

            elif answer4 == (
                "End the call and verify the request through an official channel"
            ):
                st.session_state.scenario4_correct = True
                st.session_state.beginner_score += 10
                st.rerun()

            else:
                st.error("❌ Incorrect — try again!")

                lose_image = BASE_DIR / "images" / "lose.png"

                if lose_image.exists():
                    st.image(str(lose_image), width=400)

                st.warning(
                    "The caller uses fear about visa status "
                    "to pressure you into sharing sensitive "
                    "personal information."
                )

    else:
        st.success("🎉 Correct! You identified the vishing attack!")
        st.balloons()

        win_image = BASE_DIR / "images" / "win.png"

        if win_image.exists():
            st.image(str(win_image), width=400)

        st.info(
            "Scammers may impersonate government or insurance "
            "representatives to collect passport numbers, "
            "dates of birth and policy information. "
            "Always verify unexpected requests independently."
        )

        if not st.session_state.get("popup_seen", False):
         completion_popup()
        else:
         st.metric("Final Score", f"{st.session_state.beginner_score}/40")

        if st.button("🔄 Play Beginner Again", key="restart4"):

        
            st.session_state.beginner_scenario = 1
            st.session_state.beginner_score = 0

            for number in range(1, 5):
                st.session_state[
                    f"scenario{number}_correct"
                ] = False

                st.session_state.pop(
                    f"answer{number}", None
                )

            st.rerun()

        if st.button("🏠 Back to Main Menu", key="home4"):
            st.switch_page("home.py")
