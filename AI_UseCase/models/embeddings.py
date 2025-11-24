# models/embeddings.py

# ❗ FIX: Do NOT import Streamlit or st.secrets here.
# ❗ FIX: Do NOT initialize embeddings at import time.

from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Return a lazy-loaded embeddings model."""
    return HuggingFaceEmbeddings(model_name=model_name)

# NOTE: ❌ DO NOT DO THIS:
# embeddings = get_embeddings()
# (This causes Streamlit to run before app.py)