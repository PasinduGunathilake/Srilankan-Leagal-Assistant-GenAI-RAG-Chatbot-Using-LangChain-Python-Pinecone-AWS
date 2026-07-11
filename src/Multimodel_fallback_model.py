from langsmith import traceable
from src.llm import get_ollama_llm, get_gemini_llm

# Multi-model Fallback model function
@traceable
def Multimodel_fallback():
    try:
        print(f"\n{'*'*10}Trying local LLM 1 (Ollama){'*'*10}\n")
        llm = get_ollama_llm()
        llm.invoke("test") # test ollama. Use only notebook experiment
        return llm
    except Exception as e:
        print(f"\nLLM 1 Failed: {e}. \n{'*'*10}Switching to LLM 2 (Gemini-3.5-flash){'*'*10}\n")
        return get_gemini_llm()