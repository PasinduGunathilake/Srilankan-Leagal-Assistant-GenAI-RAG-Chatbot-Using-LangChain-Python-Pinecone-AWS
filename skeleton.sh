mkdir -p src
mkdir -p research
mkdir -p data
mkdir -p assets
mkdir -p templates

touch src/__init__.py
touch src/helper.py
touch src/prompt.py
touch src/retriever.py
touch src/llm.py #(v1.0.0)
touch src/Multimodal_fallback.py #(v1.0.0)
touch src/rag_chain.py #(v1.0.0)
touch src/Guardrails.py #(v1.1.0)
touch src/embeddings.py #(v1.1.4)
touch .env
touch setup.py
touch vectorstore.py
touch research/test.ipynb
touch app.py
touch requirements.txt
touch README.md
touch CHANGELOG.md
touch LICENSE
touch .gitignore


echo "Project skeleton created successfully."
