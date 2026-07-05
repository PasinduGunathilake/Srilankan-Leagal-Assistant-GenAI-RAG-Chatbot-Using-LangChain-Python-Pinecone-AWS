from langchain_ollama import ChatOllama # this model need to be locally installed for deployment
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY NotFound!")
else:
    api_key = os.getenv("GOOGLE_API_KEY")


# LLMs
def get_ollama_llm():
    return ChatOllama(model="gemma3:1b", temperature=0.1)

def get_gemini_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY NotFound!")
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.1, # model creativity
        max_retries=3
    )

