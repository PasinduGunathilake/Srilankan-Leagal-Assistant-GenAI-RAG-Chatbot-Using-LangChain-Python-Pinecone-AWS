# 🇱🇰 Sri Lankan Legal Assistant — GenAI RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions about Sri Lankan law using LangChain, Pinecone, HuggingFace embeddings, and a locally-hosted or cloud-hosted LLM, served through a Flask web interface.

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Prerequisites](#5-prerequisites)
6. [Environment Setup](#6-environment-setup)
7. [Install Dependencies](#7-install-dependencies)
8. [Configure Environment Variables](#8-configure-environment-variables)
9. [Prepare Legal PDF Data](#9-prepare-legal-pdf-data)
10. [Build the Vector Store (One-Time Step)](#10-build-the-vector-store-one-time-step)
11. [Run the Application](#11-run-the-application)
12. [Component Breakdown](#12-component-breakdown)
    - [src/helper.py](#srchelperhpy)
    - [src/prompt.py](#srcpromptpy)
    - [src/Guardrails.py](#srcguardrailspy)
    - [src/retriever.py](#srcretrieverpy)
    - [vectorstore.py](#vectorstorepy)
    - [app.py](#apppy)
    - [templates/index.html](#templatesindexhtml)
13. [LLM Options](#13-llm-options)
14. [Guardrails Explained](#14-guardrails-explained)
15. [AWS Deployment Notes](#15-aws-deployment-notes)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Project Overview

This chatbot allows users to ask natural-language questions about Sri Lankan legislation (e.g., "What are the penalties under the Intellectual Property Act?") and receive accurate, cited answers drawn exclusively from the uploaded statutory documents.

**Key capabilities:**
- Loads, cleans, and chunks Sri Lankan legal PDFs.
- Embeds document chunks with a HuggingFace sentence-transformer model.
- Stores and retrieves vectors from a Pinecone serverless index.
- Routes user queries through an input guardrail that blocks non-legal questions.
- Passes relevant retrieved context to an LLM (local Ollama or cloud provider).
- Returns formal, source-cited legal responses via a Flask chat UI.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User (Browser)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │  HTTP POST /get
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Web App (app.py)                        │
│                                                                 │
│  1. Input Guardrail ──► Blocks non-legal queries                │
│  2. RAG Chain                                                   │
│     ├── Retriever  ──► Pinecone Vector Store (top-k=5 chunks)   │
│     └── LLM        ──► Ollama / OpenAI / Google Gemini          │
└─────────────────────────────────────────────────────────────────┘

────────────────── One-time Ingestion Pipeline ──────────────────

 Legal PDFs (data/)
      │
      ▼ load_pdf()          — DirectoryLoader + PyPDFLoader
      ▼ doc_filter()        — Noise removal & legal-signal scoring
      ▼ text_split()        — RecursiveCharacterTextSplitter (800 / 100)
      ▼ download_embeddings()— sentence-transformers/all-MiniLM-L6-v2
      ▼
 Pinecone Index ("law-rag-genai-chatbot", dim=384, cosine, AWS us-east-1)
```

---

## 3. Tech Stack

| Layer | Tool / Library |
|---|---|
| Web Framework | Flask 3.1 |
| Orchestration | LangChain 0.3 |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| Vector Database | Pinecone Serverless (AWS us-east-1) |
| LLM (local) | Ollama — `gemma3:1b` |
| LLM (cloud, optional) | OpenAI-compatible (OpenRouter) or Google Gemini |
| PDF Loader | LangChain `PyPDFLoader` / `DirectoryLoader` |
| Text Splitter | `RecursiveCharacterTextSplitter` |
| Observability | LangSmith (LangChain tracing) |
| Language | Python 3.10+ |
| Deployment | AWS (EC2 / Elastic Beanstalk) |

---

## 4. Project Structure

```
├── app.py                  # Flask application entry point
├── vectorstore.py          # One-time script: ingest PDFs → Pinecone
├── setup.py                # Package metadata
├── requirements.txt        # Python dependencies
├── skeleton.sh             # Helper script to scaffold empty project files
├── .env                    # API keys and configuration (not committed)
├── data/                   # Place your Sri Lankan legal PDF files here
├── research/
│   └── test.ipynb          # Experimental/prototyping notebook
├── src/
│   ├── __init__.py
│   ├── helper.py           # PDF loading, filtering, chunking, embeddings
│   ├── prompt.py           # System prompt template
│   ├── Guardrails.py       # Input-level guardrail (blocks non-legal queries)
│   └── retriever.py        # Loads Pinecone index and creates LangChain retriever
└── templates/
    └── index.html          # Chat UI (HTML/CSS/JS)
```

---

## 5. Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.10 or 3.11 | Recommended; avoid 3.12+ for broadest library compatibility |
| [Ollama](https://ollama.com/download) | Required for the default local LLM setup |
| Pinecone account | Free Starter tier is sufficient — [sign up](https://www.pinecone.io/) |
| LangSmith account | For request tracing — [sign up](https://smith.langchain.com/) |
| Git | To clone the repository |

> **Cloud LLM (optional):** If you prefer not to run Ollama locally, see [§13 LLM Options](#13-llm-options) for OpenRouter or Google Gemini alternatives.

---

## 6. Environment Setup

### Option A — `conda` (recommended)

```bash
conda create -n legal-chatbot python=3.10 -y
conda activate legal-chatbot
```

### Option B — `venv`

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

## 7. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/PasinduGunathilake/Srilankan-Leagal-Assistant-GenAI-RAG-Chatbot-Using-LangChain-Python-Pinecone-AWS.git
cd Srilankan-Leagal-Assistant-GenAI-RAG-Chatbot-Using-LangChain-Python-Pinecone-AWS

# Install all Python packages (includes the local src package via -e .)
pip install -r requirements.txt
```

**Key packages installed:**

| Package | Purpose |
|---|---|
| `langchain` / `langchain-core` | RAG chain orchestration |
| `langchain-pinecone` | Pinecone vector store integration |
| `langchain-ollama` | Ollama LLM integration |
| `langchain-openai` | OpenAI-compatible LLM integration |
| `langchain-community` | Community loaders and utilities |
| `sentence-transformers` | Local embedding model |
| `pypdf` | PDF parsing |
| `flask` | Web server |
| `python-dotenv` | `.env` file loading |

### Install Ollama model (for local LLM)

```bash
# Pull the default model used by the application
ollama pull gemma3:1b
```

---

## 8. Configure Environment Variables

Create a `.env` file in the project root (copy and fill in the values below):

```dotenv
# ── Pinecone ──────────────────────────────────────────────────────
PINECONE_API_KEY=your_pinecone_api_key_here

# ── LangSmith (observability / tracing) ───────────────────────────
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=sri-lankan-law-chatbot     # optional, names the project in LangSmith

# ── Cloud LLM keys (only needed if NOT using Ollama) ──────────────
OPENROUTER_API_KEY=your_openrouter_api_key_here   # for OpenRouter / OpenAI-compatible
GOOGLE_API_KEY=your_google_api_key_here            # for Google Gemini
```

> **Security:** Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 9. Prepare Legal PDF Data

Place all Sri Lankan legal PDF documents inside the `data/` directory:

```
data/
├── penal_code.pdf
├── intellectual_property_act.pdf
├── companies_act.pdf
└── ...
```

The ingestion pipeline (`src/helper.py`) will automatically:
1. Detect and load every `*.pdf` file in the directory.
2. Strip pages that match noise patterns (table of contents, gazette headers, etc.).
3. Keep only pages that contain strong or weak legal signals.
4. Split surviving pages into 800-token chunks with a 100-token overlap.

---

## 10. Build the Vector Store (One-Time Step)

Run this script **once** after adding or updating PDF files. It creates (or reuses) a Pinecone index named `law-rag-genai-chatbot` and uploads all embedded chunks.

```bash
python vectorstore.py
```

**What it does:**
1. Loads and filters PDFs from `data/` using `src/helper.py`.
2. Splits documents into chunks of ≤ 800 characters.
3. Encodes each chunk with `all-MiniLM-L6-v2` (384-dimensional vectors).
4. Creates a Pinecone Serverless index (cosine similarity, AWS `us-east-1`) if it does not already exist.
5. Upserts all document vectors into the index.

> ⚠️ **Run only when data changes.** Repeated runs will upsert duplicate vectors into Pinecone.

---

## 11. Run the Application

```bash
python app.py
```

The server starts at **http://0.0.0.0:8080** (accessible at `http://localhost:8080` in your browser).

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://<your-ip>:8080
```

Open `http://localhost:8080` to access the chat interface and start asking legal questions.

---

## 12. Component Breakdown

### `src/helper.py`

Provides four utility functions for the data ingestion pipeline:

| Function | Description |
|---|---|
| `load_pdf(path)` | Uses `DirectoryLoader` + `PyPDFLoader` to load all `*.pdf` files from a directory into LangChain `Document` objects. |
| `doc_filter(docs)` | Removes noise pages (e.g., table of contents, gazette headers) and retains only pages that match legal-specific regex patterns. |
| `text_split(doc_list)` | Splits documents into chunks of 800 characters with 100-character overlap using `RecursiveCharacterTextSplitter`. |
| `download_embeddings()` | Returns a `HuggingFaceEmbeddings` object using `sentence-transformers/all-MiniLM-L6-v2`. |

---

### `src/prompt.py`

Defines `system_prompt_text` — the system-level instruction given to the LLM on every request:

- Constrains the LLM to answer **only** from retrieved context.
- Instructs it to cite act name, section, or page number.
- Enforces formal legal language.
- Specifies a standard refusal message when no supporting context is found.

---

### `src/Guardrails.py`

Implements an **input-level rule-based guardrail** applied before any LLM call:

- `input_guardrail(query)` — checks the user's query against a list of legal keyword patterns (e.g., `act`, `law`, `court`, `penalty`, `section \d+`).
  - Returns `True` if the query appears to be legal-related → allowed through.
  - Returns `False` if the query is unrelated (e.g., "What is the weather?") → blocked with `REFUSAL_MESSAGE`.

This prevents the chatbot from answering general-knowledge or off-topic questions.

---

### `src/retriever.py`

Connects to the existing Pinecone index and creates a LangChain retriever:

| Function | Description |
|---|---|
| `load_vectorstore_index()` | Loads the Pinecone index `law-rag-genai-chatbot` using the stored embeddings. |
| `get_retriever(k=5)` | Wraps the vector store as a LangChain retriever using cosine similarity; returns the top **k** most relevant document chunks per query. |

---

### `vectorstore.py`

A **standalone one-time script** that runs the full ingestion pipeline:

1. `load_pdf` → `doc_filter` → `text_split` → `download_embeddings`
2. Initialises the Pinecone client using `PINECONE_API_KEY`.
3. Creates the serverless index if absent (384 dimensions, cosine, `aws/us-east-1`).
4. Uploads all vectorised chunks with `PineconeVectorStore.from_documents(...)`.

---

### `app.py`

The main **Flask application**:

| Component | Detail |
|---|---|
| `GET /` | Renders `templates/index.html` — the chat UI. |
| `POST /get` | Receives the user message, runs the input guardrail, invokes the RAG chain, and returns the answer as plain text. |
| `Retriever` | Initialised once at startup from `src/retriever.py`. |
| `LLM` | Default: `ChatOllama(model="gemma3:1b", temperature=0.1)`. Swap for cloud models — see [§13](#13-llm-options). |
| `prompt` | `SystemMessagePromptTemplate` (from `src/prompt.py`) + `HumanMessagePromptTemplate`. |
| `QnA_chain` | `create_stuff_documents_chain` — injects retrieved context into the prompt and calls the LLM. |
| `RAG_chain` | `create_retrieval_chain` — orchestrates the retriever and QnA chain end-to-end. |

---

### `templates/index.html`

A self-contained single-page chat interface built with HTML, CSS, and vanilla JavaScript. It sends the user's message to `POST /get` and renders the bot's response in the conversation window.

---

## 13. LLM Options

The application ships with three LLM configurations. Edit `app.py` to switch between them.

### Option 1 — Local Ollama (default)

```python
from langchain_ollama import ChatOllama

LLM = ChatOllama(
    model="gemma3:1b",
    temperature=0.1
)
```

Requires Ollama to be running locally (`ollama serve`). No API key needed.

---

### Option 2 — OpenRouter (OpenAI-compatible cloud)

```python
from langchain_openai import ChatOpenAI

LLM = ChatOpenAI(
    model="google/gemini-2.5-flash:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)
```

Requires `OPENROUTER_API_KEY` in `.env`. Free models available at [openrouter.ai](https://openrouter.ai/).

---

### Option 3 — Google Gemini (native)

```python
from langchain_google_genai import ChatGoogleGenerativeAI

LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1,
    max_retries=2
)
```

Requires `GOOGLE_API_KEY` in `.env` and `pip install langchain-google-genai`.

---

## 14. Guardrails Explained

The system implements **input-level guardrails** to ensure the chatbot stays on-topic:

```
User query
    │
    ▼
input_guardrail(query)
    ├── Legal keywords found? → True  → Proceed to RAG chain
    └── No legal keywords?   → False → Return REFUSAL_MESSAGE
```

**Detected keywords include:** `act`, `law`, `court`, `section <number>`, `penalty`, `fine`, `offence`, `constitution`, `regulation`, `minister`, `subsection`, `clause`, `tribunal`.

The LLM itself also enforces an **output-level guardrail** via the system prompt: if no relevant context is retrieved, it is instructed to respond with a standardised refusal rather than hallucinating an answer.

---

## 15. AWS Deployment Notes

The application is designed for deployment on AWS.

### Recommended: AWS EC2

```bash
# On the EC2 instance (Amazon Linux 2 / Ubuntu)
sudo apt update && sudo apt install python3-pip python3-venv -y

git clone <repo-url>
cd <repo-dir>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set environment variables (use AWS Secrets Manager or Parameter Store in production)
export PINECONE_API_KEY=...
export LANGCHAIN_API_KEY=...
export LANGCHAIN_TRACING_V2=true

# Run with gunicorn for production
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8080 app:app
```

**EC2 Security Group:** Open inbound port **8080** (or use an Application Load Balancer on port 80/443).

> For production workloads, consider running the LLM on a GPU instance or switching to a cloud-hosted model (OpenRouter / Gemini) to eliminate the local Ollama dependency.

---

## 16. Troubleshooting

| Problem | Solution |
|---|---|
| `PINECONE_API_KEY NotFound!` | Ensure `.env` is present and `PINECONE_API_KEY` is set correctly. |
| `LANGCHAIN_API_KEY NotFound!` | Add `LANGCHAIN_API_KEY` to `.env`. |
| `LANGCHAIN_TRACING_V2 not set to 'true'!` | Set `LANGCHAIN_TRACING_V2=true` in `.env`. |
| Ollama connection error | Start the Ollama daemon: `ollama serve`. Confirm the model is pulled: `ollama list`. |
| Empty answers / no results | Verify `vectorstore.py` has been run and the Pinecone index contains vectors. |
| PDFs not loading | Confirm PDF files are placed in `data/` and are not password-protected. |
| Non-legal query blocked | Expected behaviour — the input guardrail only allows legal-related questions. |

---

## Author

**Pasindu Gunathilake** — [pasindugunathilake144@gmail.com](mailto:pasindugunathilake144@gmail.com)

---

*This project is built for educational and informational purposes. It does not constitute legal advice.*

