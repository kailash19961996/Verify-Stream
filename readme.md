# VerifyStream

Developed for a Hackathon: AI Capability and Risk Demos organised by [Safe AI London](https://www.safeailondon.org/) and [Apart Research](https://www.apartresearch.com/), [VerifyStream](https://verifystream.streamlit.app/) is an AI-powered application that helps users verify the content of YouTube videos and demonstrates the dual nature of AI in combating and potentially creating misinformation.

![verifystream](https://github.com/user-attachments/assets/198b3dca-eb93-40a9-9f23-d32258f4354f)

[Click here to try the app](https://verifystream.streamlit.app/)
(Please be noted that YouTube asks for sign in while trying the app directly from Streamlit cloud. It is advisable to try it locally. More information on how to how to try it locally is shared below)


[Click here to see the 90 second demo](https://www.youtube.com/watch?v=7p44bkYDjEU)

[Visit my website for more](https://kailash.london/)

## Features

- **YouTube Video Verification**: Input any YouTube URL to analyze its content.
- **AI-Powered Analysis**: Utilizes advanced AI models to transcribe and analyze video content.
- **Fact-Checking**: Generates smart prompts and performs Google searches to verify claims.
- **Verdict Generation**: Provides a concise verdict on the truthfulness of the video content.
- **Fake News Generation**: Demonstrates how AI can be used to create convincing misinformation.

## How It Works

1. **Audio Extraction**: Downloads audio from the provided YouTube URL.
2. **Transcription**: Uses the Whisper model to transcribe the audio content.
3. **Content Analysis**: Employs GPT models to describe the video content and generate fact-checking prompts.
4. **Web Scraping**: Performs Google searches based on the generated prompts and extracts relevant information.
5. **Verification**: Analyzes the scraped data to provide a final verdict on the video's claims.
6. **Fake News Generation**: Creates an opposite narrative and generates fake news content to demonstrate AI's potential misuse.

## Technology Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - OpenAI's GPT models for text generation and analysis
  - Whisper for speech-to-text conversion
  - DALL-E for image generation
- **Web Scraping**: Google search API, Requests and BeautifulSoup
- **Audio Processing**: yt-dlp and librosa

## Setup and Usage

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your API keys in the Streamlit secrets manager:
   - OpenAI API key ([FOLLOW THIS LINK TO GET YOUR API](https://platform.openai.com/settings/organization/billing/overview))
   - Google Custom Search API key ([FOLLOW THIS LINK TO GET YOUR API](https://console.cloud.google.com/))
   - Google Search Engine ID ([FOLLOW THIS LINK TO GET YOUR ID](https://programmablesearchengine.google.com/controlpanel/all))
   - (Create a "streamlit" folder in local repo and create "secrets.toml" file inside the streamlit folder. Add the API keys in below format)
![Screenshot 2024-08-25 at 5 54 07 PM](https://github.com/user-attachments/assets/0350bec5-3ec8-4ddd-8c81-7950dd705d27)

4. Run the Streamlit app: `streamlit run main.py`

## Ethical Considerations

This app is designed to demonstrate both the potential benefits and risks of AI technology in information verification. While it can be a powerful tool for fact-checking, it also showcases how AI can be used to generate misleading content. Users are encouraged to use this tool responsibly and critically evaluate all information, regardless of its source.

## Disclaimer

This application is for educational and demonstration purposes only. The fake news generation feature is included to raise awareness about AI's potential for misuse and should not be used to create or spread misinformation.

## Contributing

Contributions to improve VerifyStream are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

[MIT License](https://opensource.org/license/mit)
