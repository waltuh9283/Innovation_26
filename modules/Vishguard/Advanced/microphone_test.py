from pathlib import Path
import streamlit as st
import speech_recognition as sr
import io

st.title("🎤 Advanced Vishing Game")

st.subheader("📞 Fake Medibank Support Call")

# Locate the scammer audio file
BASE_DIR = Path(__file__).resolve().parent

scammer_audio = BASE_DIR / "audio" / "advanced_call1.mp3"

st.write("🔊 Listen to the incoming caller.")

if scammer_audio.exists():
    st.audio(str(scammer_audio), format="audio/mpeg")
else:
    st.warning("Scammer audio file not found.")


st.warning(
    "Caller: Your OSHC account has been compromised. "
    "Please provide your verification code."
)

st.write("🎙️ Speak your response to the caller.")

audio = st.audio_input("Record Your Answer")

if audio is not None:
    st.success("Voice recorded successfully!")
    st.audio(audio)


    if st.button("🧠 Analyse My Voice"):

        recognizer = sr.Recognizer()

        try:
            audio_bytes = io.BytesIO(audio.getvalue())

            with sr.AudioFile(audio_bytes) as source:
                recorded_voice = recognizer.record(source)

            with st.spinner("Understanding your response..."):
                student_answer = recognizer.recognize_google(
                    recorded_voice,
                    language="en-AU"
                )

            st.success("Speech recognised successfully!")

            st.subheader("📝 Your Spoken Response")
            st.write(student_answer)

            
            # Evaluate the student's spoken response
            response = student_answer.lower()

            safe_phrases = [
                "will not share",
                "won't share",
                "not give",
                "won't give",
                "contact medibank",
                "call medibank",
                "official website",
                "hang up"
            ]

            unsafe_phrases = [
                "my code is",
                "the code is",
                "my password is",
                "i will give you",
                "i will share"
            ]

            if any(phrase in response for phrase in unsafe_phrases):
                st.error("⚠️ Unsafe response!")
                st.write(
                    "Never provide verification codes or "
                    "passwords to an unverified caller."
                )

            elif any(phrase in response for phrase in safe_phrases):
                st.success("✅ Correct! You avoided the scam.")
                st.write(
                    "You made a safe decision by refusing "
                    "or independently verifying the caller."
                )

            else:
                st.info("🤔 Response needs further evaluation.")
                st.write(
                    "A safe response would be to end the call "
                    "and contact Medibank through official channels."
                )


        except sr.UnknownValueError:
            st.error("Could not understand your speech. Please try again.")

        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")

        except Exception as e:
            st.error(f"Error: {e}")
