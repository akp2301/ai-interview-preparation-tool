# models/llm.py
import streamlit as st
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

def get_chatgroq_model():
    """Return a configured Groq LLM or None if missing key."""
    if not GROQ_API_KEY:
        return None

    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0.2,
        max_tokens=1024
    )