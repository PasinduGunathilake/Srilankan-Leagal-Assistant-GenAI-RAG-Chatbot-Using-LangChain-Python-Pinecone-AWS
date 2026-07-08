# ⚖️ Sri Lankan Legal AI Assistant

> A **Retrieval-Augmented Generation (RAG)** chatbot built with **LangChain · Pinecone · Ollama · Flask** — answers legal questions strictly grounded in Sri Lankan statutory documents.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-0.3.26-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Pinecone-Vector%20DB-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Ollama-gemma3%3A1b-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Flask-3.1.1-red?style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/badge/License-Educational-lightgrey?style=for-the-badge"/>
</p>

![Version](https://img.shields.io/badge/Version-1.1.0-E10600?style=for-the-badge)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Data Ingestion Pipeline](#-data-ingestion-pipeline)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [How Each Module Works](#-how-each-module-works)
- [Data Ingestion — One-Time Setup](#-data-ingestion--one-time-setup)
- [Running the Application](#-running-the-application)
- [API Reference](#-api-reference)
- [Automated LLM Failover](#-automated-llm-failover)
- [LangSmith Observability](#-langsmith-observability)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🧠 Overview

The **Sri Lankan Legal AI Assistant** is a domain-specific legal chatbot that answers questions **exclusively** from the content of Sri Lankan legal PDF documents. Leveraging **advanced AI engineering techniques**, the system implements robust **input-level guardrails** for domain safety and a **multimodal fail-safe fallback architecture** to ensure high availability. It will never hallucinate or use general world knowledge — it either finds the answer in the indexed statutes or says it cannot.
---

### 🛡️ Core Principles

| Principle | Implementation |
|-----------|---------------|
| **Grounded answers only** | LLM is restricted to the provided context via system prompt |
| **Citation-first** | Every response must reference the specific Act, section, or page |
| **Advanced Safety** | Input-level `Guardrails.py` filters non-legal queries |
| **High Availability** | `Multimodel_fallback` ensures seamless switch from Ollama to Gemini |

---

### 🚀 How it works at a high level

| Step | What happens |
|------|-------------|
| **Ingest** | PDFs are loaded, noise-filtered, chunked, and embedded into Pinecone (run once) |
| **Guard** | Every query passes through `Guardrails.py` (AI-powered filtering) to ensure domain relevance |
| **Retrieve** | Top 5 semantically similar chunks are fetched from Pinecone via `rag_chain.py` |
| **Generate** | Context-augmented prompt is sent to `gemma3:1b` (Ollama) or Gemini (Fallback) |
| **Respond** | A cited, formal legal answer is returned to the user's browser |

---

## 🏗️ System Architecture

## 🔄 Data Ingestion Pipeline

```
 data/*.pdf
     │
     ▼
 load_pdf()          — DirectoryLoader + PyPDFLoader
     │                 Reads all PDF pages into Document objects
     ▼
 doc_filter()        — Noise removal + legal signal detection
     │                 Drops TOC pages, gazette headers, price tags
     │                 Keeps pages with strong/weak legal patterns
     ▼
 text_split()        — RecursiveCharacterTextSplitter
     │                 chunk_size=800, chunk_overlap=100
     ▼
 download_embeddings() — all-MiniLM-L6-v2 (384-dim)
     │
     ▼
 Pinecone.create_index()   — cosine metric, AWS us-east-1
     │
     ▼
 PineconeVectorStore.from_documents()
     │
     ▼
 Index: "leagal-rag-ai-chatbot" ✅ Ready for retrieval
```

The ingestion pipeline (`vectorstore.py`) processes raw PDF files into searchable vector embeddings stored in Pinecone. This runs **only once** (or any time you add new documents).

---
![RAG System Architecture](images/Leagal%20GENAI%20RAG%20Chatbot.jpg)

---

## 📁 Project Structure

```
Law RAG Chatbot/
│
├── app.py                  # 🚀 Flask server — main entry point
├── vectorstore.py          # 📦 One-time ingestion: PDFs → Pinecone
├── requirements.txt        # 📋 Python dependencies
├── setup.py                # ⚙️  Package metadata (editable install)
├── .env                    # 🔑 API keys and environment variables (not committed)
├── .gitignore
├── skeleton.sh             # 🗂️  Shell script for project scaffolding
│
├── data/                   # 📄 Place Sri Lankan law PDF files here
│   └── *.pdf
│
├── src/                    # 🧩 Core application modules
│   ├── __init__.py
│   ├── helper.py           # PDF loading, filtering, chunking, embeddings
│   ├── llm.py              # 🧠 LLM factory and lazy-loading logic
│   ├── Multimodel_fallback_model.py # 🔄 Fail-safe mechanism (Ollama/Gemini)
│   ├── Guardrails.py       # 🛡️ Input-level topic safety filter
│   ├── prompt.py           # LLM system prompt template
│   ├── retriever.py        # Pinecone retriever factory
│   └── rag_chain.py        # 🔗 Core RAG orchestration and caching
│
├── templates/
│   └── index.html          # 💬 Chat web UI (Jinja2 template)
│
├── static/                 # 🎨 CSS / JS / image assets
│
└── research/               # 🔬 Jupyter notebooks (optional experiments)
```

## 🛠️ Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Web Server** | Flask 3.1.1 | Serves UI and REST API |
| **LLM1 with fail-safe mechanism** | Ollama `gemma3:1b` | Local, free, private inference |
| **LLM2 with fail-safe mechanism** | Google Gemini | Cloud-based inference options |
| **Orchestration** | LangChain 0.3.26 | Chains, retrievers, prompts |
| **Embeddings** | `all-MiniLM-L6-v2` (HuggingFace) | 384-dim semantic text vectors |
| **Vector Store** | Pinecone Serverless (AWS us-east-1) | Similarity search over legal chunks |
| **Observability** | LangSmith | Chain tracing and debugging |
| **PDF Parser** | PyPDF + LangChain DirectoryLoader | Extracts text from statutes |
| **Environment** | python-dotenv | Secure key management |
| **Packaging** | setuptools (editable install) | `src/` importable as a package |

---

## ✅ Prerequisites

Before installing, make sure you have the following:

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.10 or 3.11 | [python.org](https://python.org) |
| **Ollama** | Latest | [ollama.com](https://ollama.com) — runs the LLM locally |
| **Pinecone Account** | Free tier | [pinecone.io](https://pinecone.io) |
| **LangSmith Account** | Free tier | [smith.langchain.com](https://smith.langchain.com) |
| **Git** | Any | For cloning the repo |
| **Google API Key** | Free | [ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key) |

### Install and Configure Ollama

After installing Ollama, pull the model used by this project:

```bash
# Pull the default LLM
ollama pull gemma3:1b

# Verify it's available
ollama list
```

---

## 📦 Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/PasinduGunathilake/https://github.com/PasinduGunathilake/Srilankan-Leagal-Assistant-GenAI-RAG-Chatbot-Using-LangChain-Python-Pinecone-AWS

```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv lawvenv
lawvenv\Scripts\activate

# macOS / Linux
python -m venv lawvenv
source lawvenv/bin/activate
```

### Step 3 — Install All Dependencies

```bash
pip install -r requirements.txt
```

This installs the complete dependency set:

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | 0.3.26 | Core RAG orchestration framework |
| `langchain-core` | 0.3.66 | Base abstractions (Runnables, Documents) |
| `langchain-community` | 0.3.26 | PDF loaders, HuggingFace embeddings |
| `langchain-ollama` | 0.2.1 | Ollama LLM integration |
| `langchain-openai` | 0.3.24 | OpenAI / OpenRouter integration |
| `langchain-pinecone` | 0.2.8 | Pinecone vector store integration |
| `flask` | 3.1.1 | Web server and REST API |
| `flask-cors` | 5.0.0 | CORS support for Flask |
| `sentence-transformers` | 4.1.0 | HuggingFace embedding model runner |
| `pypdf` | 5.6.1 | PDF page extraction |
| `python-dotenv` | 1.0.0 | Loads `.env` variables at runtime |
| `ipykernel` | 7.1.0 | Jupyter support (optional) |
| `langchain_google_genai` | 2.0.10 | Gemini LLM integration |
| `-e .` | — | Editable install of this project via `setup.py` |

---

## 🔑 Configuration

### Step 4 — Set Up the `.env` File

Create or edit the `.env` file in the project root with your actual API keys:

```env
# ─── Pinecone (required) ────────────────────────────────
PINECONE_API_KEY="your-pinecone-api-key-here"

# ─── LangSmith Tracing (required) ───────────────────────
LANGCHAIN_API_KEY="your-langsmith-api-key-here"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_TRACING_PROJECT_NAME="law_rag_genai_assistant"

# ─── Cloud LLM Alternatives (Muti-model fallback system) ──────────────────
# GOOGLE_API_KEY="your-google-ai-key-here"
```

> **Where to get your keys:**
> - 🔑 **Pinecone** → [app.pinecone.io](https://app.pinecone.io) → API Keys
> - 🔑 **LangSmith** → [smith.langchain.com](https://smith.langchain.com) → Settings → API Keys
> - 🔑 **Google Gemini** → [aistudio.google.com](https://aistudio.google.com) → Get API key

> ⚠️ **Never commit your `.env` file to Git.** It is already in `.gitignore`.

---

## 🧩 How Each Module Works

### `src/helper.py` — Data Pipeline Utilities

The backbone of the ingestion pipeline. Provides four functions:

```
load_pdf() → doc_filter() → text_split() → download_embeddings()
```

| Function | What it does |
|----------|-------------|
| `load_pdf(path)` | Uses LangChain `DirectoryLoader` + `PyPDFLoader` to read all `*.pdf` files from the given directory into a list of `Document` objects |
| `doc_filter(docs)` | Removes noise pages — table of contents, gazette notices, price tags — using `NOISE_PATTERNS`. Keeps only pages matching `LEGAL_PATTERNS` (e.g., *"Act No."*, *"section 5"*) or at least 4 `WEAK_LEGAL_SIGNALS` (e.g., *"shall"*, *"court"*, *"minister"*) |
| `text_split(doc_list)` | Splits filtered documents into overlapping chunks using `RecursiveCharacterTextSplitter` — **800 character chunks** with **100 character overlap** — to preserve sentence context across boundaries |
| `download_embeddings()` | Loads `sentence-transformers/all-MiniLM-L6-v2` from HuggingFace — a fast, lightweight model that produces **384-dimensional** semantic vectors |



#### Document Filtering Logic

```
For each page in loaded PDFs:
  1. Skip pages with < 100 characters (blank / near-blank)
  2. Skip pages matching any NOISE_PATTERN (TOC, gazette header, price, etc.)
  3. KEEP if ≥ 1 LEGAL_PATTERN match (e.g., "Act No.", "section 5", "enactment")
  4. KEEP if ≥ 4 WEAK_LEGAL_SIGNAL matches (e.g., "shall", "court", "minister")
  5. Otherwise discard
```

---

### `src/prompt.py` — System Prompt

Defines `system_prompt_text` — the strict instruction template that controls LLM behaviour:

```
You are a Legal Information Assistant that ONLY handles questions related to Sri Lankan law.
Your knowledge base consists exclusively of Sri Lankan Government Acts and legal documents.

You must NEVER answer questions outside Sri Lankan legal topics, even if you have general 
knowledge about them (e.g. medicine, health, cooking, entertainment, science, technology, 
personal advice, etc.). Staying within this domain is your highest priority rule and 
overrides any instinct to be broadly helpful.

RULES (follow in order):

1. First, check if the retrieved context below contains information relevant to the query.
   - If the context contains NO information related to the query's topic, this is a strong 
     signal that the query is NOT a Sri Lankan legal matter. Proceed to Rule 4.
   - Do not use the absence of context as a reason to answer from general knowledge unless 
     you have first confirmed the query itself is a genuine Sri Lankan legal question.

2. If the answer IS found in the context, use it as your primary source of truth and cite 
   the relevant Act and Section clearly (e.g. "Section 5 of the Intellectual Property 
   (Amendment) Act").

3. If the answer is NOT found in the context, but the query is clearly a legitimate 
   Sri Lankan legal question (e.g. about an Act, legal procedure, rights, or obligations 
   under Sri Lankan law):
    a) Explicitly state that the provided documents do not contain the specific answer.
    b) Then provide a brief, high-level summary based on general legal knowledge, clearly 
       labeled as "not sourced from the provided documents" and recommending the user verify 
       with a qualified legal professional.

4. If the query is about a non-legal topic, or a topic unrelated to Sri Lankan law 
   (medicine, health, cooking, entertainment, general trivia, etc.):
    - Politely decline.
    - State clearly that you only handle Sri Lankan legal matters and cannot assist with 
      the topic asked.
    - Do NOT answer the non-legal question, even partially, even if you know the answer.
    - Do NOT provide links, summaries, or general knowledge for out-of-domain topics.

5. Maintain a professional, neutral, and helpful tone at all times.

6. Never present yourself as a substitute for a licensed Sri Lankan attorney. For complex 
   or high-stakes matters, recommend the user consult a qualified legal professional.

Context:
{context}
```

The `{context}` placeholder is filled at runtime with the retrieved document chunks.

---

### `src/Guardrails.py` — Input Safety Filter

### Guardrail Architectures and evolution

1. A **rule-based guardrail/regex guradrail** that runs before the RAG chain is invoked:
**(older version of guardrail logic, now replaced with a more robust multimodal fallback model approach in v1.1.0)**

```
User Query → input_guardrail() → True / False
                                    │         │
                                  PASS      BLOCK
                                    │         │
                                 RAG chain  REFUSAL_MESSAGE
```

| Item | Detail |
|------|--------|
| `LEGAL_PATTERNS` | Regex list: `\blaw\b`, `\bcourt\b`, `\bpenalty\b`, `\bsection\s+\d+`, `\bconstitution\b`, etc. |
| `input_guardrail(query)` | Returns `True` if ≥ 1 pattern matches the lowercased query |
| `REFUSAL_MESSAGE` | Politely declines off-topic queries without ever calling the LLM |

This prevents prompt injection attempts and keeps the system focused on its domain.


2. While we initially implemented a rule-based (Regex) filter, as of v0.0.1, we have transitioned to a more sophisticated **Multimodal Fallback Model based guardrail**(v1.1.0) to handle/filter user queries with greater contextual awareness.

```
User Query → Multimodal Guardrail (Fallback Model) → True / False
                                          │             │
                                        PASS          BLOCK
                                          │             │
                                      RAG chain   REFUSAL_MESSAGE
```

PASS: Only queries aligned with the legal domain are forwarded to the RAG chain.
BLOCK: Off-topic or prohibited queries are intercepted, returning a REFUSAL_MESSAGE without invoking the LLM.

Defines system_prompt_text — the strict instruction template that controls LLM behaviour:

```
Classify if this query relates to Sri Lankan law (Acts, IP law, GI registration, contracts, criminal law, rights, procedures, etc.)

Examples:
Query: "What is the punishment for theft under the Penal Code?" -> Yes
Query: "What are the requirements for GI registration under the IP Act?" -> Yes
Query: "What is bipolar disorder?" -> No
Query: "How to cook rice?" -> No

Query: "{query}"
```


**Architecture Comparison**

| Feature | Regex Guardrail | Multimodal Fallback Model Guardrail |
|---------|-----------------|-------------------------------------|
| `Logic Type` | Pattern matching (LEGAL_PATTERNS) | Semantic understanding & Fallback |
| `Flexibility` | Low — rigid patterns (keyword based) | High — context aware filtering(robust) |
| `prompt injection resistance` | Basic protection | High — model Advanced protection |
| `Domain Focus` | Keyword filtering | Legal query filtering |


---

### `src/retriever.py` — Pinecone Retriever Factory

Connects to the pre-populated Pinecone index and returns a LangChain-compatible retriever:

| Function | What it does |
|----------|-------------|
| `load_vectorstore_index()` | Opens the `leagal-rag-ai-chatbot` index using the same embedding model used during ingestion |
| `get_retriever(k=5)` | Returns a similarity-search retriever that fetches the **top 5** most semantically relevant chunks for a given query |

---

*in v1.0.0 Updated*
### `src/Multimodel_fallback_model.py` 
 Provides a *fail-safe mechanism*. If the primary local LLM (Ollama) fails to connect or respond, this module automatically redirects the request to a secondary cloud-based LLM (e.g., Google Gemini), ensuring system reliability.

---
*in v1.0.0 Updated*
### `src/llm.py` 
Contains factory functions for LLM initialization. Implements lazy-loading to ensure models are only initialized when needed, preventing connection errors at startup.

---

*in v1.0.0 Updated*
### `src/rag_chain.py` 
 The core orchestration module that links the LLM, prompt templates, and the Pinecone retriever. It utilizes @lru_cache to cache the Pinecone retriever instance, preventing redundant network reconnections and improving request latency. It dynamically integrates the Multimodel_fallback() mechanism, ensuring that if the local Ollama LLM fails to respond, the system seamlessly switches to a cloud-based backup (such as Google Gemini) to maintain continuous service.

---

### `vectorstore.py` — One-Time Ingestion Script

Runs the complete ingestion pipeline and uploads to Pinecone:

```
Step 1: load_pdf("./data")          → raw Document list
Step 2: doc_filter(loaded_data)     → noise-removed Document list
Step 3: text_split(filtered_data)   → chunked Document list
Step 4: download_embeddings()       → HuggingFace embedding model
Step 5: Pinecone.create_index()     → creates index if not exists
        name="leagal-rag-ai-chatbot"
        dimension=384, metric="cosine"
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
Step 6: PineconeVectorStore.from_documents() → uploads all chunks
```

---

### `app.py` — Flask Web Server (Main Entry Point)

Wires every component into a running web application:

```
Startup:
  load_dotenv() → check API keys → get_retriever() → init ChatOllama LLM
  → build ChatPromptTemplate → build QnA_chain → build RAG_chain

Routes:
  GET  /      → render_template("index.html")
  POST /get   → read msg → input_Multimodel_fallback_model_guardrail() → RAG_chain.invoke() → return answer
```

| Setting | Value |
|---------|-------|
| Host | `0.0.0.0` (all interfaces) |
| Port | `8080` |
| LLM | `ChatOllama(model="gemma3:1b", temperature=0.1)` |
| Retriever | Top-5 cosine similarity from Pinecone |

---

## 📥 Data Ingestion — One-Time Setup

### Step 5 — Add Your Legal PDF Files

Place your Sri Lankan statutory PDF documents inside the `data/` directory:

```
data/
├── intellectual_property_act.pdf
├── penal_code.pdf
├── criminal_procedure_code.pdf
├── companies_act.pdf
└── ...
```

> 💡 **Tip:** The more statutes you add, the broader the assistant's knowledge base. All PDFs in `data/` are automatically discovered and ingested.

### Step 6 — Run the Ingestion Script

> ⚠️ **Run this only once** (or when adding new PDFs). It will create and populate the Pinecone index. May take several minutes for large document sets.

```bash
python vectorstore.py
```

Expected console output:

```
Filtering 1240 documents...
kept 874/1240 (70.5%)
```

Once complete, your `leagal-rag-ai-chatbot` index in Pinecone is ready.

---

## 🚀 Running the Application

### Step 7 — Start Ollama (background service)

```bash
ollama serve
```

Keep this terminal open. Ollama must be running before starting Flask.

### Step 8 — Start the Flask Server

```bash
python app.py
```

Output:

```
 * Running on http://0.0.0.0:8080
 * Debug mode: on
```

### Step 9 — Open the Chat Interface

Navigate to **[http://localhost:8080](http://localhost:8080)** in your browser.

**Try these example queries:**

```
According to the Intellectual Property (Amendment), what is the fundamental requirement for registering a foreign geographical indication (GI) in Sri Lanka?
```

---

## � API Reference

The Flask server exposes two endpoints:

### `GET /`

Serves the chat web interface.

**Response:** `200 OK` — HTML page (`templates/index.html`)

---

### `POST /get`

Accepts a user message in JSON format and returns an AI-generated legal answer.

**Request (JSON):**
```json
{
  "msg": "What are the penalties under the Penal Code section 302?"
}

**Example (curl):**

```bash
curl -X POST http://localhost:8080/get \
     -d "msg=What are the penalties under the Penal Code section 302?"
```

**Response:**

{
  "status": "success",
  "answer": "The penalties under Section 302 are..."
}


| Status Code | Description |
|-------------|-------------|
| 200 | Success or Blocked (Guardrail) |
| 400 | Bad Request (Empty message) |
| 500 | Internal Server Error (System failure)|

> **Note:** The API always returns `200`. Error conditions are communicated as plain-text strings in the body, not HTTP error codes.

---


### 🔄 Automated LLM Failover & System Reliability
The system now features a robust **Multimodal Fallback** mechanism and **Professional Error Handling**:
- **Fail-safe mechanism:** Automatically switches between local (Ollama) and cloud (Gemini) models to ensure continuous availability.
- **Robust API communication:** Frontend and Backend now communicate via **JSON**, ensuring structured data exchange.
- **HTTP Status Codes:** The system provides meaningful HTTP status codes (200, 400, 500) to ensure the frontend can gracefully handle errors and provide user feedback.


| Model Tier | Provider | Role | Status |
|------------|----------|------|--------|
| **Primary** | Ollama | Local Inference (Privacy) | Default |
| **Secondary** | Google Gemini | Cloud Failover | Active |

#### How the Fallover Works:
1.  **Primary Attempt:** The system first attempts to connect to the local Ollama instance (e.g., `gemma3:1b`).
2.  **Health Check:** If the connection times out or the local server is down, the system immediately catches the exception.
3.  **Seamless Switch:** It automatically switches to the secondary provider (Google Gemini) to ensure your request is answered without interruption.


---
## 📊 LangSmith Observability

Every chain invocation is traced to **LangSmith**, giving you full visibility into:
- Which document chunks were retrieved
- The exact prompt sent to the LLM
- LLM latency and token usage
- Any chain errors or retries

**Dashboard:** [smith.langchain.com](https://smith.langchain.com) → Project: `law_rag_genai_assistant`

> ⚠️ If `LANGCHAIN_API_KEY` is missing or `LANGCHAIN_TRACING_V2` ≠ `"true"`, the app will **refuse to start** with a `RuntimeError`.


---

## 🔧 Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `RuntimeError: LANGCHAIN_API_KEY NotFound!` | Key missing from `.env` | Add your LangSmith API key |
| `RuntimeError: PINECONE_API_KEY NotFound!` | Key missing from `.env` | Add your Pinecone API key |
| `RuntimeError: GOOGLE_API_KEY NotFound!` | Key missing from `.env` | Add your Google API key |
| `ConnectionError` to Ollama | Ollama daemon not running | Run `ollama serve` in a terminal |
| `model not found` | Model not pulled | Run `ollama pull gemma3:1b` |
| Empty / irrelevant answers | Pinecone index not populated | Run `python vectorstore.py` first |
| Guardrail blocks a valid question | Query lacks legal keywords | Rephrase to include *law*, *court*, *act*, *section*, or *penalty* |
| Slow first response (~30s) | Embedding model downloading | `all-MiniLM-L6-v2` (~90 MB) downloads once; subsequent starts are fast |
| `ModuleNotFoundError: src` | Package not installed | Ensure you ran `pip install -r requirements.txt` (includes `-e .`) |
| Pinecone index not found | Index name typo in `retriever.py` | Confirm index name is `leagal-rag-ai-chatbot` (matches `vectorstore.py`) |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** — add new statutes to `data/`, improve filtering patterns, or enhance the UI.
3. **Test** your changes locally before submitting.
4. **Submit a Pull Request** with a clear description of what was changed and why.

### Areas open for contribution

- 📄 **Additional legal documents** — more Sri Lankan statutes
- 🔍 **Improved guardrail patterns** — better topic detection
- 🎨 **UI enhancements** — chat history, citation highlighting
- 🔧 **Alternative embedding models** — for better retrieval accuracy
- 🧪 **Test suite** — unit tests for `helper.py` and `Guardrails.py`

---

## Versioning
This project uses [Semantic Versioning](https://semver.org/). For the versions available, see the [tags on this repository](https://github.com/PasinduGunathilake/https://github.com/PasinduGunathilake/Srilankan-Leagal-Assistant-GenAI-RAG-Chatbot-Using-LangChain-Python-Pinecone-AWS/tags) or the [CHANGELOG.md](CHANGELOG.md) file.

## 👤 Author

**Pasindu Gunathilake**
📧 pasindugunathilake144@gmail.com
🔗 [GitHub](https://github.com/PasinduGunathilake)

---

## 📜 License

This project is for **educational and research purposes**.
Legal documents used must be sourced from official Sri Lankan government publications.

---
