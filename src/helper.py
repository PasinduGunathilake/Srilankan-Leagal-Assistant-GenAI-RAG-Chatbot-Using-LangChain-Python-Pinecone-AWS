from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import re
from langchain.embeddings import HuggingFaceEmbeddings

# Extract pdfs
def load_pdf(path):
    loader= DirectoryLoader(
        path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents



# filetr file content
NOISE_PATTERNS = [
    r"^list of acts",
    r"^table of contents",
    r"printed by the department",
    r"published by.*government",
    r"extraordinary gazette",
    r"price\s*:\s*rs",
    r"certified on.*\d{4}",
    r"^\s*page\s+\d+\s*$",
    r"©.*all rights reserved",
    r"can be purchased at",
    r"prakashana piyasa",
    r"compiled by lankalaw",
]

LEGAL_PATTERNS = [
    r"\bact no\.?\s*\d+",
    r"\bsection\s+\d+",
    r"\bsubsection\s*\(\d+\)",
    r"\bclause\s*\([a-z]\)",
    r"\bparagraph\s*\([ivx]+\)",
    r"\bchapter\s+[IVX]+",
    r"\bpart\s+[IVX]+",
    r"\benact(ed|s|ment)\b",
    r"\bamend(ed|ment|s)\b",
    r"\brepealed?\b",
    r"\bprovided that\b",
    r"\bnotwithstanding\b",
    r"\bwhereas\b",
    r"\bhereby\b",
    r"\bshall\b.*\b(be|have|not)\b",
    r"\bmay\b.*\b(be|make|appoint)\b",
    r"\bmeans\b.*includes?",
    r"\boffence\b.*\bpunishable\b",
    r"\bpenalty\b.*fine",
    r"\bimprisonment\b",
]

WEAK_LEGAL_SIGNALS = [
    r"\bshall\b", r"\bmay\b", r"\bmust\b", r"\bperson\b",
    r"\bauthority\b", r"\bminister\b", r"\bcourt\b", r"\btribunal\b",
]

def doc_filter(docs: List[Document]) -> List[Document]:
    filtered_docs = []
    print(f"Filtering {len(docs)} documents...")

    for doc in docs:
        text = doc.page_content.strip()
        text_lower = text.lower()

        if len(text) < 100:
            continue

        noise_matches = sum(1 for p in NOISE_PATTERNS if re.search(p, text_lower))
        if noise_matches >= 1:
            continue

        strong_legal = sum(1 for p in LEGAL_PATTERNS if re.search(p, text_lower))
        weak_legal = sum(1 for p in WEAK_LEGAL_SIGNALS if re.search(p, text_lower))

        if strong_legal >= 1 or weak_legal >= 4:
            filtered_docs.append(doc)

    print(f"kept {len(filtered_docs)}/{len(docs)} ({len(filtered_docs)/len(docs)*100:.1f}%)")
    return filtered_docs
    

# split to chunks
def text_split(doc_list):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100,
        length_function=len,
        is_separator_regex=False,
    )
    splitted_text = text_splitter.split_documents(doc_list)
    return splitted_text


# embedding model
def download_embeddings():
    model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name= model)
    return embeddings