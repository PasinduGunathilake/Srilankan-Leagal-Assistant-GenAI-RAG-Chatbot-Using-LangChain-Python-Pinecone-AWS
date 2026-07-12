from setuptools import find_packages, setup

# metadata
setup(
    name="Sri_Lankan_RAG_AI_Legal_Information_System",
    version="1.2.0", 
    author="Pasindu Gunathilake",
    author_email="pasindugunathilake144@gmail.com",
    packages=find_packages(),
    install_requires=[
        "flask",
        "langchain",
        "langchain-core",
        "langchain-ollama",
        "langchain-google-genai",
        "langchain-community",
        "langchain-pinecone",
        "python-dotenv",
        "pypdf",
        "httpx",
        "langsmith"
    ]
)

#pip install -e .