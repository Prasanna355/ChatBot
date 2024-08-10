# AI Chatbot with Wikipedia Integration

This repository contains a FastAPI backend and a Streamlit frontend that together form an AI chatbot capable of scraping Wikipedia data, processing it using vector embeddings, and answering user queries based on the retrieved information.

## Features

- **Wikipedia Scraping**: Scrape Wikipedia pages by title or URL, extract the content, and load it into a vector database for efficient retrieval.
- **Vector Embeddings**: Use HuggingFace embeddings and FAISS for similarity search over the scraped data.
- **Generative AI Model**: Query the chatbot using a powerful generative AI model to get relevant answers based on the loaded data.
- **Streamlit Frontend**: A simple and interactive user interface for loading data and querying the AI model.

## Project Structure

- **api.py**: FastAPI backend for scraping, processing, and querying data.
- **streamlit.py**: Streamlit frontend for user interaction.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Install required packages:
  ```bash
  pip install fastapi uvicorn streamlit langchain langchain-community huggingface-hub faiss-cpu requests 

Certainly! Here's the README file with the instructions formatted in code blocks:

```markdown
# AI Chatbot with Wikipedia Integration

This repository contains a FastAPI backend and a Streamlit frontend that together form an AI chatbot capable of scraping Wikipedia data, processing it using vector embeddings, and answering user queries based on the retrieved information.

## Features

- **Wikipedia Scraping**: Scrape Wikipedia pages by title or URL, extract the content, and load it into a vector database for efficient retrieval.
- **Vector Embeddings**: Use HuggingFace embeddings and FAISS for similarity search over the scraped data.
- **Generative AI Model**: Query the chatbot using a powerful generative AI model to get relevant answers based on the loaded data.
- **Streamlit Frontend**: A simple and interactive user interface for loading data and querying the AI model.

## Project Structure

- **`api.py`**: FastAPI backend for scraping, processing, and querying data.
- **`app.py`**: Streamlit frontend for user interaction.

## Setup Instructions

### Prerequisites

Ensure you have Python 3.7+ installed and then install the required packages using:

```bash
pip install requests beautifulsoup4 langchain langchain_community langchain_groq langchain-text-splitters langchain-huggingface faiss-cpu wikipedia streamlit fastapi uvicorn
```

### Running the Backend

1. **Start the FastAPI server**:

    ```bash
    uvicorn api:app --reload
    ```

2. The backend will be available at `http://localhost:8000`.

### Running the Frontend

1. **Start the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

2. The frontend will be available at `http://localhost:8501`.

## Usage

### Load Data

1. In the Streamlit app, enter the Wikipedia title or URL in the provided text input field.
2. Click the "Load Data" button.
3. The application will scrape the Wikipedia page, process the content, and load it into the vector database. A success message will be displayed upon completion.

### Query the AI Model

1. In the Streamlit app, enter your query in the provided text input field.
2. Click the "Ask" button.
3. The application will process your query using the AI model and display the generated response.

## API Endpoints

### 1. `/load` (POST)

- **Functionality**: Scrapes a Wikipedia page based on the provided title or URL, processes the data, and loads it into a FAISS index.
- **Request Body**:
    ```json
    {
      "input_text": "Wikipedia page title or URL"
    }
    ```
- **Response**:
    ```json
    {
      "status": "Data scraped, saved, and loaded into FAISS index successfully",
      "file_path": "path/to/saved/file"
    }
    ```
    or an error message if the operation fails.

### 2. `/query` (POST)

- **Functionality**: Accepts a user query, retrieves relevant data from the FAISS index, and generates an answer using the AI model.
- **Request Body**:
    ```json
    {
      "query": "Your question"
    }
    ```
- **Response**:
    ```json
    {
      "answer": "AI-generated answer based on the relevant Wikipedia data"
    }
    ```
    or an error message if the query fails.

## Development

- **FastAPI Backend**: Handles scraping, data processing, and querying. Ensure that all functions are correctly defined and that the FastAPI server is running before interacting with the frontend.
- **Streamlit Frontend**: Provides an interactive interface for users. Ensure that the Streamlit app is running to allow users to load data and query the AI model.
