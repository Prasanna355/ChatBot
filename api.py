from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
import os
from langchain.document_loaders import WikipediaLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from urllib.parse import urlparse
import traceback
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Initialize FastAPI app
app = FastAPI(title="Wikipedia QA API", description="API for querying Wikipedia content using LLM")

# Define API key for LLM (Consider using environment variables for sensitive information)
API_KEY = "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"

# Initialize LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    verbose=True,
    temperature=0.1,
    groq_api_key=API_KEY
)

# Global FAISS index
f_db = None


# Pydantic models for request bodies with input validation
class LoadModel(BaseModel):
    input_text: str

    @validator('input_text')
    def input_text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('input_text cannot be empty')
        return v


class QueryModel(BaseModel):
    query: str

    @validator('query')
    def query_not_empty(cls, v):
        if not v.strip():
            raise ValueError('query cannot be empty')
        return v


def scrape_wikipedia(input_text: str) -> tuple[str, str]:
    """
    Scrape content from Wikipedia based on the input text or URL.

    Args:
        input_text (str): The Wikipedia page title or URL.

    Returns:
        tuple: A tuple containing the page title and its content.

    Raises:
        ValueError: If no content is found on Wikipedia for the provided input.
    """
    parsed_url = urlparse(input_text)
    if parsed_url.scheme and parsed_url.netloc:
        path_parts = parsed_url.path.split('/')
        title = path_parts[-1].replace('_', ' ')
    else:
        title = input_text

    loader = WikipediaLoader(query=title, load_max_docs=1)
    data = loader.load()

    if not data:
        raise ValueError(f"No content found on Wikipedia for: {input_text}")

    return title, data[0].page_content


def save_to_file(title: str, content: str) -> str:
    """
    Save the scraped content to a file.

    Args:
        title (str): The title of the Wikipedia page.
        content (str): The content to be saved.

    Returns:
        str: The path to the saved file.
    """
    if not os.path.exists('Data'):
        os.makedirs('Data')

    filename = ''.join(c if c.isalnum() or c in [' ', '-'] else '_' for c in title)
    filename = filename.replace(' ', '_') + '.txt'
    filepath = os.path.join('Data', filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    return filepath


@app.post("/load", summary="Load Wikipedia content into FAISS index")
async def load_data(load_model: LoadModel):
    """
    Endpoint to scrape Wikipedia, save content, and load data into FAISS index.

    Args:
        load_model (LoadModel): The input model containing the Wikipedia page title or URL.

    Returns:
        dict: A status message indicating success.

    Raises:
        HTTPException: If an error occurs during the process.
    """
    global f_db
    try:
        # Scrape Wikipedia content
        title, scraped_text = scrape_wikipedia(load_model.input_text)

        # Save scraped content to a file
        saved_file = save_to_file(title, scraped_text)

        # Load data into FAISS index
        loader = TextLoader(saved_file)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20,
        )

        docs = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name='paraphrase-MiniLM-L6-v2')
        f_db = FAISS.from_documents(docs, embeddings)
        f_db.save_local("faiss_index")

        return {"status": "Data scraped, saved, and loaded into FAISS index successfully"}

    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", summary="Query the loaded Wikipedia content")
async def query_model(query: QueryModel):
    """
    Endpoint to query the loaded Wikipedia content using the LLM.

    Args:
        query (QueryModel): The input model containing the query string.

    Returns:
        dict: The answer to the query.

    Raises:
        HTTPException: If data is not loaded or an error occurs during the process.
    """
    try:
        if f_db is None:
            raise HTTPException(status_code=400, detail="Data not loaded. Please load the data first.")

        retriever = f_db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
        chatbot = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
        )

        template = """
        You are a helpful AI assistant. Your expertise is in answering queries related to Wikipedia and acting as a good conversational and customer support chatbot.

        If the question is not related to document context, kindly decline to answer.

        query: {query}

        Answer: """

        prompt = PromptTemplate(
            input_variables=["query"],
            template=template,
        )

        response = chatbot.invoke(query.query)
        return {"answer": response}

    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)