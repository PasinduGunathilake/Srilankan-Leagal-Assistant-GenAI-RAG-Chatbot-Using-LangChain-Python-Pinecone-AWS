from setuptools import find_packages, setup

# metadata
setup(
    name="sri-lankan-legal-ai-assistant",
    version="1.0.0", 
    author="Pasindu Gunathilake",
    author_email="pasindugunathilake144@gmail.com",
    packages=find_packages(),
    install_requires=[
        "flask",
        "langchain",
        "langchain-ollama",
        "langchain-google-genai",
        "langchain-community",
        "python-dotenv",
        "httpx",
        "pinecone-client",
        "langsmith"
    ]
)