
import os
from langchain_openai import ChatOpenAI

# Try to load secrets from Streamlit Cloud; fallback to local env
try:
    import streamlit as st
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
except ImportError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

from langchain_openai import ChatOpenAI

LLM_MODEL = ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
