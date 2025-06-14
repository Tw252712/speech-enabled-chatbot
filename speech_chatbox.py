
import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections

# Download NLTK data
nltk.download('punkt')

# Define chatbot conversation patterns
pairs = [
    [r"hi|hello", ["Hello!", "Hi there!"]],
    [r"how are you?", ["I'm doing well, thank you!"]],
    [r"what is your name?", ["I'm a voice-enabled chatbot (text mode active)."]],
    [r"bye", ["Goodbye!", "See you soon!"]],
    [r"(.*)", ["Tell me more!", "Why do you say that?", "Interesting..."]]
]

chatbot = Chat(pairs, reflections)

# Try importing speech recognition
try:
    import speech_recognition as sr
    HAS_SPEECH = True
except ImportError:
    HAS_SPEECH = False

# Speech recognition function
def recognize_speech():
    if not HAS_SPEECH:
        return "Speech recognition is not available (PyAudio not installed)."
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the speech."
    except sr.RequestError:
        return "Speech service error. Try again later."

# Streamlit App
def main():
    st.title("🧠 Text + Voice Chatbot")

    input_mode = st.radio("Choose Input Mode:", ("Text", "Speech"))

    if input_mode == "Text":
        user_input = st.text_input("You:")
        if st.button("Send") and user_input:
            response = chatbot.respond(user_input)
            st.text_area("Bot says:", response, height=100)

    elif input_mode == "Speech":
        if not HAS_SPEECH:
            st.error("Speech input is unavailable because `SpeechRecognition` or `PyAudio` is not installed.")
        else:
            if st.button("🎤 Speak Now"):
                user_input = recognize_speech()
                st.write(f"Transcribed: `{user_input}`")
                response = chatbot.respond(user_input)
                st.text_area("Bot says:", response, height=100)

if __name__ == "__main__":
    main()