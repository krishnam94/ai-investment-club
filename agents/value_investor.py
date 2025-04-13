from crewai import Agent
from langchain_openai import ChatOpenAI
from config import LLM_MODEL

value_investor = Agent(
    role="Value Investor",
    goal="Evaluate the fundamental value of a company using intrinsic valuation methods",
    backstory="You look for undervalued stocks based on PE ratios, book value, and long-term potential.",
    verbose=True,
    allow_delegation=False,
    llm=LLM_MODEL
)