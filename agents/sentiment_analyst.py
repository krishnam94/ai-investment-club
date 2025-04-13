from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

sentiment_analyst = Agent(
    role="Sentiment Analyst",
    goal="Analyze the tone and sentiment of recent news coverage about the stock",
    backstory="You are an expert in financial media analysis, gauging public sentiment using latest headlines.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
)