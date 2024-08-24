import streamlit as st
import yt_dlp
import os

# Function to download the audio
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '96',
        }],
        'outtmpl': 'audio.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return 'audio.mp3', "Download completed"
    except Exception as e:
        return None, str(e)

# Streamlit app
def main():
    st.title("YouTube Audio Downloader")

    youtube_url = st.text_input("Enter YouTube URL")
    
    if st.button("Download Audio"):
        if youtube_url:
            with st.spinner(f"Transcribing... This may take a while for larger files."):
                output_file, message = download_audio(youtube_url)
                if output_file:
                    st.success(message)
                    with open(output_file, 'rb') as f:
                        st.download_button('Download Audio File', f, file_name=output_file)
                    os.remove(output_file)
                else:
                    st.error(f"Error: {message}")
        else:
            st.warning("Please enter a YouTube URL")

if __name__ == "__main__":
    main()
