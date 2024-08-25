import base64
import streamlit as st
import streamlit as st
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import streamlit.components.v1 as components
import openai
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import yt_dlp
import torch
import librosa


# API's and credentials
openai.api_key = st.secrets["openai"]["api_key"]
models = ["gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
small_model = models[1]
GOOGLE_API_KEY = st.secrets["google"]["api_key"]
SEARCH_ENGINE_ID = st.secrets["google2"]["search_engine"]

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

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

def transcribe_audio(audio_file, processor, model):
    try:
        # Load audio using librosa
        audio, sr = librosa.load(audio_file, sr=16000)
        chunk_length_samples = 16000 * 30  # 30 seconds
        chunks = [audio[i:i+chunk_length_samples] for i in range(0, len(audio), chunk_length_samples)]

        transcriptions = []
        progress_bar = st.progress(0)
        for i, chunk in enumerate(chunks):
            progress_bar.progress((i + 1) / len(chunks))
            input_features = processor(chunk, sampling_rate=16000, return_tensors="pt").input_features
            forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
            with torch.no_grad():
                predicted_ids = model.generate(
                    input_features,
                    forced_decoder_ids=forced_decoder_ids,
                    max_length=448,
                )
            
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
            transcriptions.append(transcription[0])

        progress_bar.empty()
        return " ".join(transcriptions)
    except Exception as e:
        return f"Error during transcription: {str(e)}"

def get_gpt4_response(prompt, gpt_model = small_model):
    response = openai.ChatCompletion.create(
        model= gpt_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    return response['choices'][0]['message']['content']

def describe_statement(text):
    prompt = f"Provide a very brief description of what this video is about:\n\n\"{text}\""
    response = get_gpt4_response(prompt)
    return response.strip()

def generate_fact_check(text):
    prompt = f"""
    Based on the given text, generate a set of 1-2 search prompts that can be used to 
    verify the claims and find comprehensive, factual information about the subject. 
    Each prompt should:
    1.Focus on a specific claim or feature mentioned in the text
    2.Be phrased as a clear, concise question or statement that encourages fact-checking
    3.Seek evidence, reviews, or expert opinions to corroborate the information
    4.Include elements of comparison with similar technologies or services where appropriate
    5.Be suitable for use in a search engine to find reliable, authoritative sources
    6.Ensure that the prompts are designed to critically examine the claims made.

    given text : {text}

    Output only the prompt and nothing else.
    No numbering and no empty lines.
    """
    response = get_gpt4_response(prompt, gpt_model = small_model)
    response = [line.strip() for line in response.splitlines() if line.strip()]
    return response

def google_search(query, api_key, cse_id, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None
    
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        # st.error(f"Failed to extract content from {url}: {e}")
        return ""

def summarize_text(query, text):
    prompt = f"""
    Video context: 
    \"{query}\".
    The google search results: 
    \"{text}\"
    Based on the google search results and your existing knowledge, give me a very brief response about how true the context of the video is.
    """
    response = get_gpt4_response(prompt)
    return response.strip()

def generate_opposite_narrative(user_input):
    prompt = f"Create a narrative that directly contradicts or opposes the following statement:\n\n\"{user_input}\". Output only the title and nothing else."
    response = get_gpt4_response(prompt)
    return response.strip()

def generate_fake_news(opposite_narrative):
    prompt_title = f"Generate a sensational news headline based on this narrative:\n\n\"{opposite_narrative}\". Output only the title and nothing else. Format it in New York Times style"
    prompt_content = f"Write a fake news article based on the narrative:\n\n\"{opposite_narrative}\". Output only the fake news article and nothing else. Format it in New York Times style"
    
    fake_news_title = get_gpt4_response(prompt_title)
    fake_news_content = get_gpt4_response(prompt_content)
    return fake_news_title.strip(), fake_news_content.strip()

def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

