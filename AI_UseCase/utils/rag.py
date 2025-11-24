# utils/rag.py
import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import embeddings from models/embeddings.py
try:
    from models.embeddings import embeddings
except Exception:
    # fallback: lazy import to avoid import errors in tests
    from models.embeddings import get_embeddings
    embeddings = get_embeddings()

DATA_PATH = "data/interview_guide.txt"
INDEX_DIR = "data/faiss_index"

@st.cache_resource(ttl=24 * 3600)
def build_or_load_index(index_dir: str = INDEX_DIR):
    """Return FAISS index; build and save if missing."""
    try:
        # If saved index exists, load it
        if os.path.exists(index_dir) and os.listdir(index_dir):
            return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

        # Build index
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"RAG data file not found at {DATA_PATH}")

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw_text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)
        chunks = splitter.split_text(raw_text)

        index = FAISS.from_texts(chunks, embeddings)

        # Save local index for fast future loads
        os.makedirs(index_dir, exist_ok=True)
        index.save_local(index_dir)

        return index

    except Exception as e:
        # Re-raise as RuntimeError so callers can catch generically
        raise RuntimeError(f"Error building/loading RAG index: {e}") from e


def retrieve_context(query: str, k: int = 3) -> str:
    """Return concatenated top-k contexts for the query, or empty string on error."""
    try:
        index = build_or_load_index()
        results = index.similarity_search(query, k=k)
        context = "\n\n".join([r.page_content for r in results if getattr(r, "page_content", "").strip()])
        return context
    except Exception:
        # If anything goes wrong, return empty string (safe fallback)
        return ""