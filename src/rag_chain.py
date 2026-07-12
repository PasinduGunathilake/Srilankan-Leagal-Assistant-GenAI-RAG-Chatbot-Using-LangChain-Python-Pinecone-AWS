from src.prompt import *
from src.retriever import get_retriever, get_reranked_retriever 
from src.Multimodel_fallback_model import Multimodel_fallback
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv
from functools import lru_cache
import os


load_dotenv()

if not os.getenv("LANGCHAIN_API_KEY"):
    raise RuntimeError("LANGCHAIN_API_KEY NotFound!")

if os.getenv("LANGCHAIN_TRACING_V2") != "true":
    raise RuntimeError("LANGCHAIN_TRACING_V2 not set to 'true'!")

# Cache the retriever to prevent reconnection issues on each request/reload
@lru_cache(maxsize=1)
def get_cached_retriever():
    return get_retriever()


#chains/pipeline

def get_chains():

    # Brain(model)
    # Call mutlimodal_fallback_model
    LLMs = Multimodel_fallback()

    # prompt template
    system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)
    human_prompt = HumanMessagePromptTemplate.from_template("{input}")

    prompt = ChatPromptTemplate.from_messages(
        [
            system_prompt,
            human_prompt
        ]
    )
    '''
    old method

    QnA_chain = create_stuff_documents_chain(llm=LLMs, prompt=prompt)
    RAG_chain = create_retrieval_chain(get_cached_retriever(), QnA_chain)
    '''
    QnA_chain = create_stuff_documents_chain(llm=LLMs, prompt=prompt)
    Retriever = get_cached_retriever()

    # RAG pipeline
    def RAG_chain(user_query):
        #retrieve
        raw_data = Retriever.invoke(user_query)
        #rerank
        Retrived_reranked_docs = get_reranked_retriever(input_query=user_query, retrieved_data=raw_data)
        #context prepare
        context_docs = [res['content'] for res in Retrived_reranked_docs]
        #answer
        response = QnA_chain.invoke({
            "context": context_docs,
            "input": user_query
        })

        return response, context_docs

    return RAG_chain

