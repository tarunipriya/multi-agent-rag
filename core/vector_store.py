from langchain_chroma import Chroma
from core.embeddings import get_embeddings

def get_vector_store(collection_name="research"):
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    return vector_store

def get_retriever(collection_name="research", top_k=5):
    vector_store = get_vector_store(collection_name)
    return vector_store.as_retriever(
        search_kwargs={"k": top_k}
    )