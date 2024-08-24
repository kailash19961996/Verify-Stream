import streamlit as st
import tempfile
import os
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa

# Load Whisper model and processor
@st.cache_resource
def load_whisper_model():
    processor = AutoProcessor.from_pretrained("openai/whisper-tiny")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny")
    return processor, model

def transcribe_audio_chunk(audio_chunk, processor, model):
    input_features = processor(audio_chunk, sampling_rate=16000, return_tensors="pt").input_features
    
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
    
    with torch.no_grad():
        predicted_ids = model.generate(
            input_features,
            forced_decoder_ids=forced_decoder_ids,
            max_length=448,
        )
    
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription[0]

def transcribe_audio(audio_file):
    processor, model = load_whisper_model()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as temp_audio_file:
        temp_audio_file.write(audio_file.read())
        temp_audio_file_path = temp_audio_file.name

    try:
        # Load audio using librosa
        audio, sr = librosa.load(temp_audio_file_path, sr=16000)

        # Process audio in chunks
        chunk_length_samples = 16000 * 30  # 30 seconds
        chunks = [audio[i:i+chunk_length_samples] for i in range(0, len(audio), chunk_length_samples)]

        transcriptions = []
        progress_bar = st.progress(0)
        for i, chunk in enumerate(chunks):
            progress_bar.progress((i + 1) / len(chunks))
            transcription = transcribe_audio_chunk(chunk, processor, model)
            transcriptions.append(transcription)

        progress_bar.empty()
        return " ".join(transcriptions)
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None
    finally:
        os.unlink(temp_audio_file_path)

def main():
    st.title("Audio Transcription App")
    st.write("Upload an audio file to transcribe it to text.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("Transcribe"):
            with st.spinner("Transcribing... This may take a while for larger files."):
                transcription = transcribe_audio(uploaded_file)
            
            if transcription:
                st.subheader("Transcription:")
                st.text_area("Transcription result", value=transcription, height=300)
                
                st.download_button(
                    label="Download Transcription",
                    data=transcription,
                    file_name="transcription.txt",
                    mime="text/plain",
                )

if __name__ == "__main__":
    main()