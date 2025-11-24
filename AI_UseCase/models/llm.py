# models/llm.py
import streamlit as st
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

def get_chatgroq_model():
    """Return a configured Groq LLM or None if missing key."""
    if not GROQ_API_KEY:
        st.error("❌ No GROQ API key found. Please set it in Streamlit Secrets.")
        return None

    return ChatGroq(
        model="mixtral-8x7b-32768",
        api_key=GROQ_API_KEY,
    )
