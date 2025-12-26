from langchain_pinecone import PineconeVectorStore
from src.prompt import system_prompt_text as system_prompt_text
from vectorstore import Embeddings, index_name
from langchain_ollama import ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv
import os


load_dotenv()
if not os.getenv("LANGCHAIN_API_KEY"):
    raise RuntimeError("LANGCHAIN_API_KEY NotFound!")

if os.getenv("LANGCHAIN_TRACING_V2") != "true":
    raise RuntimeError("LANGCHAIN_TRACING_V2 not set to 'true'!")


# load data from vectorstore
doc_search = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=Embeddings
)

# retriever
Retriever = doc_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k":5}
)

# Brain(model)
LLM = ChatOllama(
    model="gemma3:1b",
    temperature=0.1
)

# prompt template
system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)
human_prompt = HumanMessagePromptTemplate.from_template("{input}")

prompt = ChatPromptTemplate.from_messages(
    [
        system_prompt,
        human_prompt
    ]
)

#chains
QnA_chain = create_stuff_documents_chain(llm=LLM, prompt=prompt)
RAG_chain = create_retrieval_chain(Retriever, QnA_chain)


question = "what punishments of intellectual property law in sri lanka?"
response = RAG_chain.invoke({"input":question})
print(response['answer'])