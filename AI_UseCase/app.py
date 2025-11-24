# app.py
import streamlit as st
st.set_page_config(
    page_title="LangChain Multi-Provider ChatBot",
    page_icon="🤖",
    layout="wide"
)

import os
import sys

# allow running from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from models.llm import get_chatgroq_model
from utils.rag import retrieve_context
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.web_search import tavily_search


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
        chat_model = get_chatgroq_model()
        if chat_model is None:
            st.error("❌ No GROQ API key found. Please add it in secrets.toml")

        # FIXED: Using llm instead of chat_model
        response = chat_model.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"

def instructions_page():
    st.title("📘 How to Use the AI Interview Coach")

    st.markdown("""
Welcome to the **AI Interview Preparation Tool**!  
This chatbot is designed to help you practice interviews, learn concepts fast, and get high-quality answers in two modes: **Concise** and **Detailed**.  

---

## 🚀 Features
### **1. Smart Interview Chatbot**
Ask anything related to:
- Python, SQL, DevOps  
- MLOps, Cloud (Azure, AWS, GCP)  
- DSA fundamentals  
- Behavioral questions  
- System design  
- Role-specific interviews  

Select your preferred response mode:
- **Concise** → crisp, short interview-ready answers  
- **Detailed** → long explanations + examples

---

## 🔍 2. Built-in RAG (Knowledge Retrieval)
The system automatically searches your internal knowledge base and uses it to generate better answers.

You don’t need to do anything — the chatbot detects and retrieves relevant context in the background.

---

## 🌐 3. Built-in Web Search  
You can perform a live web search by typing:


Examples:
- `search: latest features in Azure DevOps`
- `search: What is Groq Llama3 model?`
- `search: Kubernetes vs Docker 2025`

The bot will fetch and summarize results for you.

---

## 💬 4. Chat History
Your conversation history is preserved in the session.

Click **🗑 Clear Chat History** anytime from the sidebar.

---

## 🔧 5. Requirements
Before using the chatbot fully:
- Add your **Groq API Key** in `.env` or Streamlit Secrets.
- Ensure your folder structure remains unchanged.
- Keep your internet connection on for web search.

---

## 🧠 Tips for Best Results
- Ask *1 clear question at a time* for the most accurate answer.
- When preparing for interviews, try questions like:
  - *“Explain CI/CD like I’m a beginner.”*
  - *“Give me STAR-based answers for: Tell me about yourself.”*
  - *“Mock interview me for a DevOps role.”*
  - *“Explain Kubernetes architecture with diagram-style text.”*

---

## 🎯 Goal of this Tool
This project showcases:
- Generative AI integration  
- LangChain message formatting  
- RAG workflow  
- External Web Search  
- Streamlit UI design  
- Multi-provider model support (Groq, OpenAI, HuggingFace)

Perfect for interview prep and as a portfolio project.

---

If you have any issues, return to the **Chat** page and ask the bot anything!


""")

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
