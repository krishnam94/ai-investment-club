
import os
from langchain_openai import ChatOpenAI

# Set your API key as an environment variable or paste it here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPER_API_KEY")
# LLM configuration
LLM_MODEL = ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
