from langchain.embeddings import HuggingFaceEmbeddings

# initialoze embedding model as gloal varable for efficient memory usage
_embedding_model = None

# embedding model download
def get_downloaded_embeddings():
    global _embedding_model
    if _embedding_model is None:
        print(f"{'*'*10} Initializing Embeddings ... {'*'*10}\n")
        model = "sentence-transformers/all-MiniLM-L6-v2"
        _embedding_model = HuggingFaceEmbeddings(model_name= model)
    return _embedding_model