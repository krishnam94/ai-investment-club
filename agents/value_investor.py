from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

value_investor = Agent(
    role="Value Investor",
    goal="Evaluate the fundamental value of a company using intrinsic valuation methods",
    backstory="You look for undervalued stocks based on PE ratios, book value, and long-term potential.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)
)