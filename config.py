import os
from langchain_openai import ChatOpenAI

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Initialize the LLM with a faster model
LLM_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=500,
    streaming=False  # Disable streaming for faster responses
)
