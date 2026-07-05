from langsmith import traceable
from src.llm import get_ollama_llm, get_gemini_llm

# Multi-model Fallback model function
@traceable
def Multimodel_fallback():
    try:
        print(f"{'*'*10}Trying local LLM 1 (Ollama){'*'*10}")
        llm = get_ollama_llm()
        llm.invoke("Hi") # test call
        return llm
    except Exception as e:
        print(f"LLM 1 Failed: {e}. \n{'*'*10}Switching to LLM 2 (Gemini-3.5-flash){'*'*10}")
        return get_gemini_llm()