import streamlit as st
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os
import streamlit.components.v1 as components
import openai
from background import add_bg_from_local, describe_statement, generate_fact_check, generate_fact_check, google_search, extract_text_from_url, summarize_text, generate_opposite_narrative, generate_fake_news, generate_image, download_audio, transcribe_audio, get_gpt4_response

add_bg_from_local('images/bg5.jpg')

linkedin = "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/linkedin.gif"
github =   "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/gitcolor.gif"
Youtube =  "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/371907120_YOUTUBE_ICON_TRANSPARENT_1080.gif"
email =    "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/emails33.gif"
website =  "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/www.gif"

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

col1, col2 = st.columns([1, 3])
with col1:
    spline_component("https://lottie.host/embed/c723a9ba-2211-4763-8577-5ef32f97a869/yNF4aB95zv.json")

with col2:
    st.title("Verify Stream")

coll1,coll2,coll3 = st.columns(3)
with coll2:
    st.write(
        f"""
            <div style='display: flex; align-items: center;'>
            <a href = 'https://kailash.london/'><img src='{website}' style='width: 45px; height: 45px; margin-right: 25px;'></a>
            <a href = 'https://www.youtube.com/@kailashbalasubramaniyam2449/videos'><img src='{Youtube}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href = 'https://www.linkedin.com/in/kailash-kumar-balasubramaniyam-62b075184'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href = 'https://github.com/kailash19961996'><img src='{github}' style='width: 30px; height: 30px; margin-right: 25px;'></a>
            <a href = 'mailto:kailash.balasubramaniyam@gmail.com''><img src='{email}' style='width: 31px; height: 31px; margin-right: 25px;'></a>
        </div>""", unsafe_allow_html=True,)
    
st.markdown("""
<div style='text-align: center;'>
     <i>"Verify YouTube video claims with ease, or see how AI can twist facts—this app is a double-edged tool for truth and misinformation."<i>
     <h4>90-second Demo</h4>
</div>
""", unsafe_allow_html=True)

# https://www.youtube.com/watch?v=7p44bkYDjEU

video_id = "7p44bkYDjEU"
youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=0&mute=0"
st.markdown(f"""
    <style>
        .video-outer-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding-top: 1px; 
        }}
        .video-container {{
            position: relative;
            width: 50%;
            padding-bottom: 28.125%;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 15px;
        }}
    </style>
    <div class="video-outer-container">
        <div class="video-container">
            <iframe src="{youtube_embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    </div>
""", unsafe_allow_html=True)

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
                with st.spinner("Describing Video..."):
                    description = describe_statement(transcription)
                    st.subheader("Video Description")
                    st.write(description)

                prompts = generate_fact_check(transcription)
                st.subheader("Smart Prompts")
                st.write(prompts)

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
                with st.spinner("Making final verdict..."):
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
        
        else:
            st.error("Couldn't extract audio")
                        
        
        # Clean up the temporary audio file
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
    else:
        st.warning("Please enter a YouTube URL")

st.markdown("""
<div style='text-align: center;'>
    Built by Kai. Like this? <a href="https://kailash.london/">Hire me!</a>
</div>
""", unsafe_allow_html=True)
