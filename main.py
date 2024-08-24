import streamlit as st
from pytube import YouTube
import openai
import whisper
import os
import traceback

# Set up OpenAI API Key
openai.api_key = 'your_api_key_here'

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    try:
        return whisper.load_model("tiny")
    except Exception as e:
        st.error(f"Error loading Whisper model: {str(e)}")
        st.error(traceback.format_exc())
        return None

model = load_whisper_model()

def extract_captions(youtube_url):
    try:
        yt = YouTube(youtube_url)
        captions = yt.captions.get_by_language_code('en')
        if captions:
            return captions.generate_srt_captions()
        else:
            return None
    except Exception as e:
        st.error(f"Error extracting captions: {str(e)}")
        return None

def extract_audio_and_transcribe(youtube_url):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(filename='temp_audio')
        
        if model is not None:
            result = model.transcribe(audio_file)
            os.remove(audio_file)  # Clean up the audio file after processing
            return result['text']
        else:
            st.error("Whisper model is not loaded. Unable to transcribe.")
            return None
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def main():
    st.title("VerifyStream")
    st.write("Provide a YouTube link to extract and display captions or transcribed audio.")

    youtube_url = st.text_input("YouTube URL")

    if youtube_url:
        st.write("Processing...")
        captions = extract_captions(youtube_url)

        if captions:
            st.subheader("Extracted Captions:")
            st.text_area("Captions", captions, height=300)
        else:
            st.write("No captions found. Extracting and transcribing audio...")
            transcribed_text = extract_audio_and_transcribe(youtube_url)
            if transcribed_text:
                st.subheader("Transcribed Text from Audio:")
                st.text_area("Transcription", transcribed_text, height=300)

if __name__ == "__main__":
    main()