from langchain_pinecone import PineconeVectorStore
from src.embeddings import get_downloaded_embeddings
from src.reranker import get_downloaded_reranker 

# initialize embeddings
Embeddings = get_downloaded_embeddings()

# initialize reranker
Rerank = get_downloaded_reranker()

# vector index name
index_name = "leagal-rag-ai-chatbot"

# load data from vectorstore
def load_vectorstore_index():
    doc_search = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=Embeddings
    )
    return doc_search
    

# retriever function (old/new - previously used without re-ranking)

def get_retriever(k: int=20):
    doc_search= load_vectorstore_index()
    Retriever = doc_search.as_retriever(
        search_type="similarity",  # which means retrieve data base on cosine similarity
        search_kwargs={"k":k}
    )
    return Retriever


# retriver function with reranking

def get_reranked_retriever(input_query, retrieved_data,top_n=3):

    pairs = [(input_query, doc.page_content) for doc in retrieved_data]
    scores = Rerank.predict(pairs)

    results = []
    for i in range(len(retrieved_data)):
        results.append({
            "content": retrieved_data[i],
            "score": scores[i]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_n]