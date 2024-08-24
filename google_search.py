import streamlit as st
import requests
import openai
from bs4 import BeautifulSoup

# Set up your Google Custom Search API credentials
API_KEY = "AIzaSyDd6clxZcueZXGGRySfubDm0NXAZyG1xVY"
SEARCH_ENGINE_ID = "d5319dcfff9d64fb6"

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
    For the given Query: 
    \"{query}\"
    give a brief response based on the given text
    \"{text}\"
    """
    response = get_gpt4_response(prompt)
    return response.strip()


def main():
    st.title('Web Search Summarizer')

    query = st.text_input('Enter your search query:')

    if st.button("Search"):
        if query:
            with st.spinner('Searching...'):
                results = google_search(query, API_KEY, SEARCH_ENGINE_ID, num=2)

                if results is None:
                    st.error("Failed to get results. Please check your API key and Search Engine ID.")
                elif 'error' in results:
                    st.error(f"API Error: {results['error']['message']}")
                elif 'items' in results:
                    contents = []
                    for item in results['items']:
                        st.subheader(item['title'])
                        st.write(item['link'])

                        # Extract and summarize content from the URL
                        content = extract_text_from_url(item['link'])
                        if content:
                            contents.append(content)

                    # Combine summaries into one final summary
                    if contents:
                        final_summary = summarize_text(query, ' '.join(contents))
                        st.subheader("Final Summary")
                        st.write(final_summary)
                else:
                    st.write('No results found for this query.')


if __name__ == "__main__":
    main()
