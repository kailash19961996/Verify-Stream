import streamlit as st
from pytube import YouTube
import os

# Function to download the audio
def download_audio(youtube_url):
    try:
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path='.', filename='audio.mp4')
        return output_file, yt.title
    except Exception as e:
        return None, str(e)

# Streamlit app
def main():
    st.title("YouTube Audio Downloader")

    youtube_url = st.text_input("Enter YouTube URL")
    
    if st.button("Download Audio"):
        if youtube_url:
            output_file, message = download_audio(youtube_url)
            if output_file:
                st.success(f"Download successful: {message}")
                with open(output_file, 'rb') as f:
                    st.download_button('Download Audio File', f, file_name=f'{message}.mp4')
            else:
                st.error(f"Error: {message}")
        else:
            st.warning("Please enter a YouTube URL")

if __name__ == "__main__":
    main()
