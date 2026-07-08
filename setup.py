from setuptools import find_packages, setup

# metadata
setup(
    name="sri-lankan-legal-ai-assistant",
    version="1.1.1", 
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