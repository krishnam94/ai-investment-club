from crewai import Agent
from config import LLM_MODEL

sentiment_analyst = Agent(
    role="Sentiment Analyst",
    goal="Analyze the tone and sentiment of recent news coverage about the stock",
    backstory="You are an expert in financial media analysis, gauging public sentiment using latest headlines.",
    verbose=True,
    allow_delegation=False,
    llm=LLM_MODEL
)