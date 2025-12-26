#for store vectors in vector database. run only ones
from src.helper import load_pdf, doc_filter, text_split, download_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("PINECONE_API_KEY"):
    raise RuntimeError("PINECONE_API_KEY NotFound!")

# data preprocessing chain
loaded_data = load_pdf("./data")
filtered_data = doc_filter(loaded_data)
chunked_data = text_split(filtered_data)

# initialize embeddings
Embeddings = download_embeddings()

# vector db initialize
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

# db indexing
index_name = "law-rag-genai-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric ="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# store embedded chunks
doc = PineconeVectorStore.from_documents(
    documents = chunked_data,
    embedding = Embeddings,
    index_name = index_name
)