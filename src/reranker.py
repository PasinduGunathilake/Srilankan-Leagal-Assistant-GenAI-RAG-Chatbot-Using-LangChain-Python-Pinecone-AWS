from sentence_transformers import CrossEncoder
import torch
from functools import lru_cache

# re-ranking model download

# Cache the reranker to prevent reconnection issues on each request/reload
@lru_cache(maxsize = 1)
def get_downloaded_reranker():
     # GPU availability check
    if torch.cuda.is_available() == True:
        device = "cuda"
    else:
        device = "cpu"
    print(f"{'#'*10} Reranker running device: {device} {'#'*10}")

    model = "cross-encoder/ms-marco-MiniLM-L6-v2"
    rerank_model = CrossEncoder(
        model_name = model,
        device = device
    )

    return rerank_model