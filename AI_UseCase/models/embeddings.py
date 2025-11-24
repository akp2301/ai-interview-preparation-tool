# models/embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings

# Factory + module-level instance so old imports still work
def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Return a HuggingFaceEmbeddings instance.
    Keep this in models/ so the assignment expects it here.
    """
    return HuggingFaceEmbeddings(model_name=model_name)

# module-level default (import this from other modules)
embeddings = get_embeddings()