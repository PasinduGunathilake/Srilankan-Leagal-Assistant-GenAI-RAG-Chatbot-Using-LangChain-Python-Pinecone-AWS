#!/bin/bash
# For store Ollama models use Persistent Storage
export OLLAMA_MODELS=/data/.ollama/models
ollama serve & 
sleep 10
ollama pull gemma3:1b
python app.py