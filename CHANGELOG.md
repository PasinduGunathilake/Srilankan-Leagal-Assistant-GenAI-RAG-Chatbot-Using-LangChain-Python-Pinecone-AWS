# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-07-08
### Added
- **JSON API Integration:** Refactored backend communication to use JSON for robust and scalable data exchange.
- **Enhanced Error Handling:** Implemented proper HTTP status codes (200, 400, 500) for better frontend-backend synchronization.
- **Professional User Feedback:** Standardized response messages for system-blocked queries.
- **Code Optimization:** Cleaned up redundant logic and removed unreachable code in `app.py`.
- **Comprehensive Documentation:** Added professional comments throughout the codebase for maintainability.

### Changed
- **Advanced Guardrail Implementation:** Migrated from basic Regex-based guardrails to a more robust Multimodal Fallback model approach (adder in previous version - again used same in this) for smarter, context-aware input filtering.



## [1.0.0] - 2026-07-06
### Added
- *Multimodal Fallback:* Integrated a fail-safe mechanism (Ollama + Gemini) to ensure system reliability.
- *Modular Architecture:* Fully refactored the codebase into distinct modules (rag_chain.py, llm.py, etc.) for better maintainability.
- *Safety Features:* Enhanced input-level guardrails to ensure safe and relevant responses.

### Changed
- *Codebase Refactoring:* Reorganized the project structure for improved scalability and clean code standards.
- *Resource Management:* Implemented lazy-loading for LLM initialization to prevent connection errors and optimize memory usage.
- *Configuration:* Improved dependency management and environment variable handling.




## [0.0.1] - 2026-03-02/ 2026-07-04
### Added
- Intergrated input level guardrails for user queries to ensure safe and relevant responses.
- Updated the Guarlrail.py file to optimize the guardrail logic and improve performance.




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

