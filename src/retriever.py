from langchain_pinecone import PineconeVectorStore
from src.helper import download_embeddings 

# initialize embeddings
Embeddings = download_embeddings()

# vector index name
index_name = "leagal-rag-ai-chatbot"

# load data from vectorstore
def load_vectorstore_index():
    doc_search = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=Embeddings
    )
    return doc_search
    

# retriever function
def get_retriever(k: int=5):
    doc_search= load_vectorstore_index()
    Retriever = doc_search.as_retriever(
        search_type="similarity",
        search_kwargs={"k":k}
    )
    return Retriever