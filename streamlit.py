import streamlit as st
import requests
from streamlit_lottie import st_lottie
from typing import Optional, Dict, Any

# Function to load Lottie animation from a URL
def load_lottie(url: str) -> Optional[Dict[str, Any]]:
    """
    Load a Lottie animation from a given URL.

    Args:
        url (str): The URL of the Lottie animation JSON.

    Returns:
        Optional[Dict[str, Any]]: The Lottie animation as a dictionary, or None if loading fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to load Lottie animation: {e}")
        return None

# Set page config
st.set_page_config(page_title="AI Chatbot Interface", page_icon="🤖", layout="wide")

# Load Lottie animations from URLs
LOTTIE_BOT_URL = "https://lottie.host/42f43994-cfc6-4408-ab63-da5f95aaf949/BEmmUhY81B.json"
LOTTIE_LOADING_URL = "https://lottie.host/4ab98ed0-11f8-4326-a610-f1e57a084160/lorWdGfryP.json"

lottie_bot = load_lottie(LOTTIE_BOT_URL)
lottie_loading = load_lottie(LOTTIE_LOADING_URL)

# Custom CSS
st.markdown("""
<style>
.big-font {
    font-size: 30px !important;
    font-weight: bold;
}
.stTextInput>div>div>input {
    font-size: 18px;
}
.stButton>button {
    font-size: 18px;
    font-weight: bold;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Title and description
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="big-font">AI Chatbot Interface</p>', unsafe_allow_html=True)
    st.write("Ask questions about any Wikipedia article!")
with col2:
    if lottie_bot:
        st_lottie(lottie_bot, height=150, key="bot_animation")

# Create tabs
tab1, tab2 = st.tabs(["Load Data", "Ask Questions"])

# Function to make API requests
def make_api_request(endpoint: str, data: Dict[str, str]) -> requests.Response:
    """
    Make an API request to the specified endpoint.

    Args:
        endpoint (str): The API endpoint to call.
        data (Dict[str, str]): The data to send in the request body.

    Returns:
        requests.Response: The response from the API.
    """
    try:
        response = requests.post(f"http://localhost:8000/{endpoint}", json=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

with tab1:
    st.header("Load Wikipedia Data")
    wiki_input = st.text_input("Enter the Wikipedia title or URL to scrape and load:", key="wiki_input")
    if st.button("Load Data", key="load_button"):
        if not wiki_input.strip():
            st.warning("Please enter a Wikipedia title or URL.")
        else:
            with st.spinner("Scraping and loading data..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="loading_animation")
                load_response = make_api_request("load", {"input_text": wiki_input})
                if load_response and load_response.status_code == 200:
                    st.success("Data scraped, saved, and loaded into Milvus DB successfully!")
                elif load_response:
                    st.error(f"Error loading data: {load_response.text}")

with tab2:
    st.header("Ask Your Question")
    query = st.text_input("Enter your query:", key="query_input")
    if st.button("Ask", key="ask_button"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("Processing your query..."):
                response = make_api_request("query", {"query": query})
                if response and response.status_code == 200:
                    st.info("Response:")
                    st.write(response.json().get("answer"))
                elif response:
                    st.error(f"Error: {response.text}")

# Add a footer
st.markdown("---")
