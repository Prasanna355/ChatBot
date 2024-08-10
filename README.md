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
