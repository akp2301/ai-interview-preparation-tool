# app.py
import streamlit as st
import os
import sys
from dotenv import load_dotenv

# allow running from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from models.llm import get_chatgroq_model
from utils.rag import retrieve_context
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.web_search import tavily_search

load_dotenv()

def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model with RAG + Web Search support."""
    try:
        user_query = messages[-1]["content"]  # Last user message

        # ============================
        # 🔍 1. Check for Web Search
        # ============================
        if "search:" in user_query.lower():
            search_term = user_query.split("search:", 1)[1].strip()
            search_results = tavily_search(search_term)
            return f"🔍 **Web Search Results for:** `{search_term}`\n\n{search_results}"

        # ============================
        # 2. RAG Context Retrieval
        # ============================
        rag_context = retrieve_context(user_query)

        system_message_content = f"""
You are an AI Interview Coach.

Response Mode: {system_prompt}

If relevant, use the following retrieved context from the knowledge base:
{rag_context}
"""

        formatted_messages = [
            SystemMessage(content=system_message_content)
        ]

        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_messages.append(AIMessage(content=msg["content"]))

        # 3. LLM Response
                # 3. LLM Response
        llm = get_chatgroq_model()
        if llm is None:
            return "⚠️ Cannot generate response: Missing API key."

        # FIXED: Using llm instead of chat_model
        response = llm.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"

def instructions_page():
    st.title("The Chatbot Blueprint")
    st.markdown("...")  # keep your long instructions here

def chat_page():
    st.title("🤖 AI ChatBot")

    mode = st.radio("Response Mode:", ["Concise", "Detailed"])
    system_prompt = "Provide short, crisp, interview-ready answers." if mode == "Concise" else "Provide detailed, explanatory, teaching-style answers with examples."

    chat_model = get_chatgroq_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your message here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Getting response..."):
                response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    if chat_model is None:
        st.info("🔧 No valid Groq API key found. Please add it inside config/config.py or .env.")

def main():
    st.set_page_config(page_title="LangChain Multi-Provider ChatBot", page_icon="🤖", layout="wide")
    with st.sidebar:
        page = st.radio("Go to:", ["Chat", "Instructions"], index=0)
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    if page == "Instructions":
        instructions_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
