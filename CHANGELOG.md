# Changelog

All notable changes to this project will be documented in this file.

## [1.1.3] - 2026-07-10
### Added
- **Docker Compose Orchestration:** Migrated to a robust multi-container architecture (Web App + Ollama) for local and server deployment.
- **Persistent Storage:** Configured Docker volumes to ensure persistent data storage for AI models.
- **Environment Configuration:** Added `OLLAMA_BASE_URL` to `.env` to support seamless switching between local and containerized environments.

### Changed
- **Deployment Strategy:** Removed `entrypoint.sh` in favor of a cleaner Docker Compose startup process.
- **Infrastructure:** Updated `Dockerfile` and `docker-compose.yml` for production-grade reliability.



## [1.1.2] - 2026-07-09
### Added
- **Cloud Deployment Optimization:** Configured `app.py` for dynamic port binding and secure production mode using environment variables.
- **Infrastructure:** Created `entrypoint.sh` to handle automated service initialization (Ollama + Flask) within the Docker container.
- **Documentation:** Updated `README.md` and `CHANGELOG.md` to reflect the latest project status and cloud-ready architecture.

### Changed
- **Deployment Strategy:** Optimized Dockerfile structure for production deployment on Render.com.


## [1.1.1] - 2026-07-08
### Fixed
- Resolved dependency conflict between `pinecone-client` and `pinecone`.
- Updated `requirements.txt` to include compatible dependency versions.
- update some codelines


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

