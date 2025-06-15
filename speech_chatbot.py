import streamlit as st
import speech_recognition as sr
import os

# -------------------------
# Initialize Session State
# -------------------------
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "status_msg" not in st.session_state:
    st.session_state.status_msg = ""

# -------------------------
# Sidebar Settings
# -------------------------
st.sidebar.title("🛠️ Settings")

api_choice = st.sidebar.selectbox(
    "Select Speech Recognition API",
    ["Google", "Sphinx"]
)

language = st.sidebar.text_input("Language Code (e.g., en-US, fr-FR)", value="en-US")

filename = st.sidebar.text_input("Save Transcription As", value="transcription.txt")

# -------------------------
# Main UI
# -------------------------
st.title("🎙️ Real-Time Speech Recognition")

st.markdown("Use the buttons below to control speech recognition.")

col1, col2, col3, col4 = st.columns(4)
start = col1.button("▶️ Start")
pause = col2.button("⏸️ Pause")
resume = col3.button("🔄 Resume")
stop = col4.button("⏹️ Stop")

save = st.button("💾 Save Transcription")

# Status and output
st.subheader("📝 Transcription Output")
output_box = st.text_area("Your transcribed text will appear here:", 
                          value=st.session_state.transcribed_text, 
                          height=300)

status = st.empty()
if st.session_state.status_msg:
    status.info(st.session_state.status_msg)

# -------------------------
# Core Transcription Logic
# -------------------------
recognizer = sr.Recognizer()
mic = sr.Microphone()

def transcribe_once():
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            status.info("🎧 Listening...")
            audio = recognizer.listen(source, timeout=5)
            status.info("🧠 Recognizing...")

            if api_choice == "Google":
                text = recognizer.recognize_google(audio, language=language)
            elif api_choice == "Sphinx":
                text = recognizer.recognize_sphinx(audio, language=language)
            else:
                text = "[Invalid API selection]"

            st.session_state.transcribed_text += text + "\n"
            st.session_state.status_msg = "✅ Transcribed successfully!"
            st.experimental_rerun()

    except sr.WaitTimeoutError:
        st.session_state.status_msg = "⌛ Timeout. Please speak again."
    except sr.UnknownValueError:
        st.session_state.status_msg = "🤷 Could not understand the audio."
    except sr.RequestError as e:
        st.session_state.status_msg = f"❌ API error: {e}"
    except Exception as e:
        st.session_state.status_msg = f"⚠️ Error: {e}"
    finally:
        st.experimental_rerun()

# -------------------------
# Button Actions
# -------------------------
if start:
    st.session_state.is_listening = True
    st.session_state.status_msg = "🎤 Started listening..."
    transcribe_once()

if pause:
    st.session_state.is_listening = False
    st.session_state.status_msg = "⏸️ Paused."

if resume:
    st.session_state.is_listening = True
    st.session_state.status_msg = "🔄 Resumed listening..."
    transcribe_once()

if stop:
    st.session_state.is_listening = False
    st.session_state.status_msg = "🛑 Stopped listening."

if save:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(st.session_state.transcribed_text)
        st.success(f"📁 Transcription saved to '{filename}'")
    except Exception as e:
        st.error(f"❌ Error saving file: {e}")
