# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str) -> str:
    return os.getenv(key)

GROQ_API_KEY = get_env("GROQ_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")
