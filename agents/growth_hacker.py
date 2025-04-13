from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

growth_hacker = Agent(
    role="Growth Hacker",
    goal="Identify high-growth opportunities based on tech trends and earnings potential",
    backstory="You specialize in spotting breakout stocks in tech, biotech, and emerging markets.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
)