# config/config.py
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_env(key: str) -> str:
    try:
        # Use Streamlit secrets ONLY if available
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass  # Ignore Streamlit errors locally

    # 2. Fallback to local .env
    return os.getenv(key)

GROQ_API_KEY = get_env("GROQ_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")
