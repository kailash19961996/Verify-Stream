import openai
import pandas as pd
import streamlit as st

openai.api_key = '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'
models = ["gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
small_model = models[1]
smart_model = models[1]

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
    prompt = f"Provide a brief description of what this statement is about:\n\n\"{text}\""
    response = get_gpt4_response(prompt)
    return response.strip()

def segment_text_with_context(text):
    prompt = f"Segment the following text into meaningful statements, and focus only on those that are verifiable facts. Ignore any taunts, rants, or personal attacks. Provide only the verifiable statements in multiple paragraphs separated by double newlines, without any numbering:\n\n\"{text}\""
    response = get_gpt4_response(prompt)
    segments = response.split("\n\n")  # Split by paragraphs, assuming GPT returns segments separated by double newlines
    st.subheader("segments")
    st.write(segments)
    return [segment.strip() for segment in segments if segment.strip()]

def generate_fact_check(segment):
    prompt = f"""
    For the following segment:

    \"{segment}\"

    If the segment contains factual information that can be verified, provide only the fact-checking prompt without any additional text or prefixes.
    The fact-checking prompts should be in format that can be used to do google search.
    If the segment is a joke, taunt, or something that cannot be verified, simply respond with "Cannot be verified".
    """
    response = get_gpt4_response(prompt, gpt_model = smart_model)
    return response.strip()

@st.cache_data
def create_fact_check_table(text):
    segments = segment_text_with_context(text)
    
    data = []
    for segment in segments:
        fact_check = generate_fact_check(segment)
        data.append({
                'Concept': segment,
                'Fact-Check': fact_check
            })
            
    
    df = pd.DataFrame(data)
    return df

def main():
    st.title("Fact-Checkable Elements Extractor")
    
    # Input text area
    text = st.text_area("Enter the statement", height=100)
    
    if st.button("Analyze"):
        if text:
            description = describe_statement(text)
            st.subheader("Statement Description")
            st.write(description)
            
            df = create_fact_check_table(text)
            st.subheader("Fact-Checkable Elements")
            
            # Show only the first 10 rows initially
            st.dataframe(df.head(10))
            
            # Optionally, allow the user to expand to view more rows
            if len(df) > 10:
                if st.button("Load More"):
                    st.dataframe(df)
        else:
            st.warning("Please enter a statement.")

if __name__ == "__main__":
    main()