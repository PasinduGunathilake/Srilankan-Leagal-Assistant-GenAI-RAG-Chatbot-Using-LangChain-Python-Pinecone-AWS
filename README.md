# ⚖️ Sri Lankan Law AI Assistant

> A **Retrieval-Augmented Generation (RAG)** chatbot built with LangChain, Pinecone, Ollama, and Flask — designed to answer legal questions strictly grounded in Sri Lankan statutory documents.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [How Each Module Works](#how-each-module-works)
- [Data Ingestion (One-Time Setup)](#data-ingestion-one-time-setup)
- [Running the Application](#running-the-application)
- [Switching LLM Backends](#switching-llm-backends)
- [LangSmith Tracing](#langsmith-tracing)
- [Troubleshooting](#troubleshooting)

---

## Overview

The **Sri Lankan Law AI Assistant** is a domain-specific chatbot that answers legal questions using only the content of uploaded Sri Lankan legal PDF documents. It uses a RAG pipeline to:

1. **Load & clean** legal PDFs from a local `data/` directory.
2. **Chunk & embed** the cleaned text using a HuggingFace sentence-transformer model.
3. **Store** the embeddings in a Pinecone vector database (done once).
4. At query time, **retrieve** the most relevant document chunks and pass them — along with the user's question — to a local LLM (Ollama `gemma3:1b` by default).
5. **Enforce** topic-focused safety via an input-level guardrail that blocks non-legal queries.
6. **Serve** the answer through a Flask web UI.

---

## Architecture

```
User Browser
     │
     ▼
┌─────────────────────────────────────┐
│            Flask Web Server         │  app.py
│  GET /  →  index.html               │
│  POST /get  →  RAG pipeline         │
└────────────────┬────────────────────┘
                 │
        Input Guardrail
        (Guardrails.py)
                 │ (legal query only)
                 ▼
┌─────────────────────────────────────┐
│           RAG Chain                 │
│  LangChain RetrievalQA              │
│  ┌──────────────┐  ┌─────────────┐  │
│  │   Retriever  │  │    LLM      │  │
│  │  (Pinecone)  │  │  (Ollama)   │  │
│  └──────────────┘  └─────────────┘  │
└───────────┬─────────────────────────┘
            │
┌───────────▼──────────────┐
│   Pinecone Vector Store  │  (pre-populated via vectorstore.py)
│   Index: law-rag-genai-  │
│   chatbot  (dim=384)     │
└──────────────────────────┘
```

---

## Project Structure

```
Law RAG Chatbot/
│
├── app.py                  # Flask server — main entry point
├── vectorstore.py          # One-time script: ingest PDFs → Pinecone
├── requirements.txt        # Python dependencies
├── setup.py                # Package metadata (pip editable install)
├── .env                    # API keys and environment settings
├── .gitignore
│
├── data/                   # Place your Sri Lankan law PDF files here
│
├── src/                    # Core application modules
│   ├── __init__.py
│   ├── helper.py           # PDF loading, filtering, chunking, embeddings
│   ├── prompt.py           # System prompt template
│   ├── retriever.py        # Pinecone retriever factory
│   └── Guardrails.py       # Input-level topic guardrail
│
├── templates/
│   └── index.html          # Chat web UI
│
├── static/                 # CSS / JS assets for the web UI
│
└── research/               # Experimental notebooks (optional)
```

---

## Tech Stack

| Component | Technology |
|---|---|
| **Web Framework** | Flask |
| **LLM (default)** | Ollama (`gemma3:1b`) — runs locally |
| **LLM (alternatives)** | OpenRouter (OpenAI-compatible) · Google Gemini |
| **Orchestration** | LangChain |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| **Vector Database** | Pinecone (Serverless, AWS `us-east-1`) |
| **Observability** | LangSmith tracing |
| **PDF Parsing** | PyPDF via LangChain `DirectoryLoader` |
| **Environment** | Python `python-dotenv` |

---

## Environment Setup

### Prerequisites

| Requirement | Version / Notes |
|---|---|
| Python | 3.10 or 3.11 recommended |
| Ollama | [Install from ollama.com](https://ollama.com) — required for the default LLM |
| Pinecone account | Free tier is sufficient — [pinecone.io](https://pinecone.io) |
| LangSmith account | Free — [smith.langchain.com](https://smith.langchain.com) |

### 1. Pull the Ollama Model

After installing Ollama, pull the default model used by the app:

```bash
ollama pull gemma3:1b
```

Verify it is available:

```bash
ollama list
```

---

## Installation

### 2. Clone the Repository

```bash
git clone https://github.com/PasinduGunathilake/Srilankan-LAW-Assistant-GenAI-RAG-Chatbot-Using-LangChain-Python-Pinecone-Streamlit-AWS.git
cd "Law RAG Chatbot"
```

### 3. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv lawvenv
lawvenv\Scripts\activate

# macOS / Linux
python -m venv lawvenv
source lawvenv/bin/activate
```

### 4. Install All Dependencies

```bash
pip install -r requirements.txt
```

This installs the following packages:

| Package | Purpose |
|---|---|
| `langchain==0.3.26` | Core RAG orchestration framework |
| `langchain-core==0.3.66` | LangChain base abstractions |
| `langchain-community==0.3.26` | Community integrations (PDF loaders, HuggingFace embeddings) |
| `langchain-ollama==0.2.1` | Ollama LLM integration |
| `langchain-openai==0.3.24` | OpenAI / OpenRouter LLM integration |
| `langchain-pinecone==0.2.8` | Pinecone vector store integration |
| `flask==3.1.1` | Web server framework |
| `flask-cores` | Flask CORS support |
| `sentence-transformers==4.1.0` | HuggingFace embedding model |
| `pypdf==5.6.1` | PDF text extraction |
| `python-dotenv==1.0.0` | Load `.env` variables at runtime |
| `ipykernel==7.1.0` | Jupyter notebook support (optional) |
| `-e .` | Installs the project itself as an editable package via `setup.py` |

---

## Configuration

### 5. Set Up the `.env` File

Create or edit the `.env` file in the project root:

```env
# Pinecone — required for vector store
PINECONE_API_KEY="your-pinecone-api-key-here"

# LangSmith — required for tracing
LANGCHAIN_API_KEY="your-langsmith-api-key-here"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_TRACING_PROJECT_NAME="law_rag_genai_assistant"

# Only needed if using OpenRouter (optional)
# OPENROUTER_API_KEY="your-openrouter-api-key-here"

# Only needed if using Google Gemini (optional)
# GOOGLE_API_KEY="your-google-api-key-here"
```

> **Get your keys:**
> - Pinecone API Key → [app.pinecone.io](https://app.pinecone.io) → API Keys section
> - LangSmith API Key → [smith.langchain.com](https://smith.langchain.com) → Settings → API Keys

---

## How Each Module Works

### `src/helper.py` — Data Pipeline Utilities

Provides four functions used by `vectorstore.py` during data ingestion:

| Function | Description |
|---|---|
| `load_pdf(path)` | Recursively loads all `*.pdf` files from the given directory using LangChain's `DirectoryLoader` + `PyPDFLoader`. Returns a list of `Document` objects. |
| `doc_filter(docs)` | Filters out noise pages (e.g., table of contents, gazette headers, price tags) using `NOISE_PATTERNS`. Keeps only pages that contain legal language, detected by `LEGAL_PATTERNS` (strong signals like "Act No.", "section 5") or multiple `WEAK_LEGAL_SIGNALS` (e.g., "shall", "court"). |
| `text_split(doc_list)` | Splits documents into overlapping chunks using `RecursiveCharacterTextSplitter` with `chunk_size=800` and `chunk_overlap=100` characters. |
| `download_embeddings()` | Loads the `sentence-transformers/all-MiniLM-L6-v2` model from HuggingFace. This 384-dimensional model converts text chunks into semantic vectors. |

---

### `src/prompt.py` — System Prompt

Defines `system_prompt_text`, a strict instruction template injected before every LLM call. The prompt enforces:
- Answer **only** from retrieved documents.
- Cite act name, section, or page number from context.
- Use formal legal language.
- Never use external knowledge outside the provided `{context}`.

---

### `src/Guardrails.py` — Input Safety Filter

Implements a **rule-based input guardrail** that runs before the RAG chain:

- `LEGAL_PATTERNS`: A list of regex patterns (e.g., `\blaw\b`, `\bcourt\b`, `\bpenalty\b`, `\bsection\s+\d+`) that indicate a legal-related question.
- `input_guardrail(query)`: Returns `True` if at least one legal pattern matches the (lowercased) query; otherwise returns `False`.
- If the guardrail returns `False`, the app returns `REFUSAL_MESSAGE` immediately — the LLM is never invoked.

---

### `src/retriever.py` — Pinecone Retriever

Connects to the existing Pinecone index and exposes it as a LangChain retriever:

- `load_vectorstore_index()`: Opens the `law-rag-genai-chatbot` index in Pinecone using the same HuggingFace embedding model used during ingestion.
- `get_retriever(k=5)`: Returns a similarity-search retriever that fetches the top **5** most relevant document chunks for a given query.

---

### `vectorstore.py` — One-Time Data Ingestion Script

Orchestrates the full data pipeline to populate Pinecone **once**:

1. Load PDFs from `./data` → `load_pdf()`
2. Filter noise → `doc_filter()`
3. Chunk text → `text_split()`
4. Create embeddings → `download_embeddings()`
5. Connect to Pinecone and create the `law-rag-genai-chatbot` index (dimension=384, cosine metric, AWS us-east-1 serverless) if it doesn't already exist.
6. Upload all embedded chunks to the index via `PineconeVectorStore.from_documents()`.

---

### `app.py` — Flask Web Server (Main Entry Point)

Initialises and wires all components together:

| Component | Description |
|---|---|
| **LLM** | `ChatOllama(model="gemma3:1b", temperature=0.1)` — deterministic, locally-run |
| **Prompt** | `ChatPromptTemplate` combining `SystemMessagePromptTemplate` (from `prompt.py`) and `HumanMessagePromptTemplate` |
| **RAG Chain** | `create_stuff_documents_chain` → `create_retrieval_chain` — retrieves context, stuffs it into the prompt, invokes the LLM |
| `GET /` | Renders `templates/index.html` — the chat web UI |
| `POST /get` | Accepts `msg` form field → validates with guardrail → runs RAG chain → returns text answer |

The server listens on `0.0.0.0:8080`.

---

## Data Ingestion (One-Time Setup)

### 6. Add Your Legal PDF Documents

Place all Sri Lankan law PDF files inside the `data/` directory:

```
data/
├── intellectual_property_act.pdf
├── penal_code.pdf
├── criminal_procedure_code.pdf
└── ...
```

### 7. Run the Vector Store Ingestion Script

> ⚠️ **Run this only once** (or whenever you add new documents). This will upload vectors to Pinecone and may take a few minutes depending on the number and size of PDFs.

```bash
python vectorstore.py
```

You will see output similar to:

```
Filtering 1240 documents...
kept 874/1240 (70.5%)
```

After this step, your Pinecone index `law-rag-genai-chatbot` will be populated and ready for querying.

---

## Running the Application

### 8. Start Ollama (Keep Running in Background)

```bash
ollama serve
```

### 9. Start the Flask Server

```bash
python app.py
```

The server starts on:

```
http://localhost:8080
```

Open your browser and navigate to `http://localhost:8080` to use the chat interface.

**Example legal queries:**
- *"What are the punishments for intellectual property offences under Sri Lankan law?"*
- *"Explain section 15 of the Penal Code."*
- *"What does the court have the power to do under the Criminal Procedure Code?"*

---

## Switching LLM Backends

The `app.py` file has commented-out alternatives ready to use:

### Option A: OpenRouter (Cloud, Free Tier Available)

```python
from langchain_openai import ChatOpenAI

LLM = ChatOpenAI(
    model="google/gemini-2.5-flash:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)
```

Add `OPENROUTER_API_KEY` to your `.env` file.

### Option B: Google Gemini (Cloud)

```python
from langchain_google_genai import ChatGoogleGenerativeAI

LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1,
    max_retries=2
)
```

Add `GOOGLE_API_KEY` to your `.env` file and install the extra package:

```bash
pip install langchain-google-genai
```

---

## LangSmith Tracing

This project is pre-configured to log every chain invocation to **LangSmith**, giving you full visibility into retrieval steps, prompt construction, and LLM responses.

- **Dashboard**: [smith.langchain.com](https://smith.langchain.com)
- **Project name**: `law_rag_genai_assistant` (set in `.env`)
- Tracing is enabled via `LANGCHAIN_TRACING_V2=true`

If `LANGCHAIN_API_KEY` or `LANGCHAIN_TRACING_V2` is missing or incorrect, the app will **refuse to start** and raise a `RuntimeError`.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `RuntimeError: LANGCHAIN_API_KEY NotFound!` | `.env` file missing or key empty | Add your LangSmith API key to `.env` |
| `RuntimeError: PINECONE_API_KEY NotFound!` | Pinecone key missing | Add `PINECONE_API_KEY` to `.env` |
| `ConnectionError` to Ollama | Ollama is not running | Run `ollama serve` in a separate terminal |
| Model not found by Ollama | Model not pulled yet | Run `ollama pull gemma3:1b` |
| Empty responses / bad retrieval | Vectors not ingested | Run `python vectorstore.py` first |
| Guardrail blocks a valid query | Query lacks legal keywords | Rephrase to include words like *law*, *court*, *act*, *section*, *penalty* |
| Slow first response | Embedding model downloading | The first run downloads `all-MiniLM-L6-v2` (~90 MB); subsequent runs are fast |

---

## Author

**Pasindu Gunathilake**
📧 pasindugunathilake144@gmail.com

---

## License

This project is for educational and research purposes. The legal documents used must be obtained from official Sri Lankan government sources.
