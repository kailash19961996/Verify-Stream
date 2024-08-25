import streamlit as st
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os
import streamlit.components.v1 as components
import openai
from background import add_bg_from_local, describe_statement, generate_fact_check, generate_fact_check, google_search, extract_text_from_url, summarize_text, generate_opposite_narrative, generate_fake_news, generate_image, download_audio, transcribe_audio, get_gpt4_response

add_bg_from_local('images/bg5.jpg')

# Custom CSS to force white text color and style the menu bar
st.markdown("""
    <style>
    /* Target main content area */
    .main .block-container {
        color: white !important;
    }
    
    /* Ensure headers are white */
    .main .block-container h1, 
    .main .block-container h2, 
    .main .block-container h3, 
    .main .block-container h4, 
    .main .block-container h5, 
    .main .block-container h6 {
        color: Red !important;
    }
    
    /* Make sure paragraphs and lists are white */
    .main .block-container p,
    .main .block-container li {
        color: white !important;
    }
    
    /* Style for text input (URL input) */
    .main .block-container .stTextInput input {
        background-color: black !important;
        color: white !important;
        border: 1px solid Gray !important;
    }

    /* Ensure the label for text areas is white */
    .main .block-container .stTextArea label,
    .main .block-container .stTextInput label {
        color: white !important;
    }
    
    /* Style for file uploader text */
    .main .block-container .stFileUploader label {
        color: white !important;
    }
    
    /* Style for buttons */
    .stButton > button {
        background-color: black !important;
        color: white !important;
        border: 1px solid White !important;
    }
    
    /* Hover effect for buttons */
    .stButton > button:hover {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid Red !important;
    }

    /* Style for download button */
    .stDownloadButton > button {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }
    
    /* Hover effect for download button */
    .stDownloadButton > button:hover {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* Style for the menu bar */
    .stApp header {
        background-color: black !important;
        color: white !important;
    }

    /* Style for menu items */
    .stApp header button {
        color: white !important;
    }

    /* Hover effect for menu items */
    .stApp header button:hover {
        background-color: #333 !important;
    }

    /* Style for hamburger menu icon */
    .stApp header [data-testid="stDecoration"] {
        background-color: white !important;
    }

    /* Style for the sidebar */
    .css-1544g2n.e1fqkh3o4 {
        background-color: black !important;
    }

    /* Style for sidebar items */
    .css-1544g2n.e1fqkh3o4 .streamlit-expanderHeader,
    .css-1544g2n.e1fqkh3o4 .streamlit-expanderContent {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# App header
def spline_component(url, width=150, height=90):
    components.iframe(url, width=width, height=height)

col1, col2 = st.columns([1, 4])
with col1:
    spline_component("https://lottie.host/embed/c723a9ba-2211-4763-8577-5ef32f97a869/yNF4aB95zv.json")

with col2:
    st.title("Verify Stream")

# API's and credentials
openai.api_key = st.secrets["openai"]["api_key"]
models = ["gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
small_model = models[1]
GOOGLE_API_KEY = st.secrets["google"]["api_key"]
SEARCH_ENGINE_ID = st.secrets["google2"]["search_engine"]

# Essential functions
# Load Whisper model and processor
@st.cache_resource
def load_whisper_model():
    processor = AutoProcessor.from_pretrained("openai/whisper-tiny")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny")
    return processor, model

# Streamlit App   
youtube_url = st.text_input("Enter YouTube URL")
if st.button("Verify"):
    if youtube_url:
        with st.spinner("Downloading audio... This may take a while."):
            output_file, message = download_audio(youtube_url)
            if output_file:
                with st.spinner("Extracting text from audio..."):
                    processor, model = load_whisper_model()
                    transcription = transcribe_audio(output_file, processor, model)

                    if transcription:
                        # st.text_area("Extracted Text", value=transcription, height=100)
                        description = describe_statement(transcription)
                        st.subheader("Video Description")
                        st.write(description)

                        prompts = generate_fact_check(transcription)
                        # st.subheader("Prompts")
                        # st.write(prompts)

                        # Searching google
                        with st.spinner('Googling...'):
                            st.subheader("Google Search Results")
                            contents = []
                            for query in prompts:
                                results = google_search(query, GOOGLE_API_KEY, SEARCH_ENGINE_ID, num=2)

                                if results is None:
                                    st.error("Failed to get results. Please check your API key and Search Engine ID.")
                                elif 'error' in results:
                                    st.error(f"API Error: {results['error']['message']}")
                                elif 'items' in results:
                                    for item in results['items']:
                                        st.write(item['title'])
                                        st.write(item['link'])

                                        # Extract and summarize content from the URL
                                        content = extract_text_from_url(item['link'])
                                        if content:
                                            contents.append(content[:10000])
                                else:
                                    st.write('No results found for this query.')

                            # Combine summaries into one final summary
                            final_summary = summarize_text(description, ' '.join(contents))
                            st.subheader("Verdict")
                            st.write(final_summary)

                            # Creating Fake news
                            with st.spinner("Creating fake news..."):
                                opposite_narrative = generate_opposite_narrative(description)
                                fake_news_title, fake_news_content = generate_fake_news(opposite_narrative)
                                with st.spinner("Creating images..."):
                                    image_prompt = f"An illustration for a news article: {fake_news_title}"
                                    image = generate_image(image_prompt)

                            # Display outputs
                            # st.subheader("Opposite Narrative")
                            # st.write(opposite_narrative)

                            st.subheader("Fake News")
                            st.subheader(fake_news_title)
                            st.image(image, caption=fake_news_title, width=256)
                            
                            paragraphs = fake_news_content.split('\n\n', 5) 
                            if len(paragraphs) > 2:
                                intro_content = paragraphs[0] + '\n\n' + paragraphs[1] + '\n\n' + paragraphs[2] + '\n\n' + paragraphs[3] + '\n\n' + paragraphs[4]
                                extended_content = paragraphs[5]
                            else:
                                intro_content = fake_news_content
                                extended_content = ""

                            st.write(intro_content) 
                            if extended_content:
                                with st.expander("Read More"):
                                    st.markdown(extended_content)
                    else:
                        st.error("Transcription failed.")
                        
        # Clean up the temporary audio file
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
    else:
        st.warning("Please enter a YouTube URL")
