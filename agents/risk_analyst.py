from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

risk_analyst = Agent(
    role="Risk Analyst",
    goal="Identify and explain financial and geopolitical risks in a given stock",
    backstory="You are a cautious and analytical investment advisor who specializes in identifying downside risks.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
)