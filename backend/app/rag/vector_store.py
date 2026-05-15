import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=get_embeddings()
    )

def get_retriever(domain: str = None):
    vector_store = get_vector_store()
    search_kwargs = {"k": 8}
    if domain:
        search_kwargs["filter"] = {"domain": domain}
    return vector_store.as_retriever(search_kwargs=search_kwargs)
