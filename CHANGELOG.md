# Changelog

All notable changes to this project will be documented in this file.

## [0.0.0] - 2025-12-27
### Added
- Initial project setup and architecture.
- Integrated **Ollama** with `gemma3:1b` model as the primary LLM.
- Configured **Pinecone** vector store for document retrieval.
- Initialized local embedding support using `HuggingFaceEmbeddings`.
- Implemented data ingestion pipelines and retrieval chain.
- Implemented Flask API for serving the RAG chatbot.
- Enhanced with UI and chat functionlities.
- **Langsmith** integrated for Monitoring.

## [0.0.1] - 2026-03-02/ 2026-07-04
### Added
- Intergrated input level guardrails for user queries to ensure safe and relevant responses.
- Updated the Guarlrail.py file to optimize the guardrail logic and improve performance.
