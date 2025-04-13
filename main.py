from crewai import Crew, Task
from agents.risk_analyst import risk_analyst
from agents.value_investor import value_investor
from agents.growth_hacker import growth_hacker
from agents.sentiment_analyst import sentiment_analyst
from langchain_openai import ChatOpenAI
from tools.news_sentiment import fetch_news

from config import OPENAI_API_KEY, SERPAPI_KEY
import sys
# Define a mock stock to evaluate
stock = sys.argv[1] if len(sys.argv) > 1 else "NVIDIA"

# Tasks
risk_task = Task(
    description=f"Analyze the potential financial and geopolitical risks of investing in {stock}.",
    expected_output="A list of top 3 risks with short justifications.",
    agent=risk_analyst
)

value_task = Task(
    description=f"Evaluate whether {stock} is undervalued or overvalued based on its financials and fundamentals.",
    expected_output="A short valuation opinion with key financial metrics.",
    agent=value_investor
)

growth_task = Task(
    description=f"Analyze the growth potential of {stock} over the next 2-3 years based on market trends.",
    expected_output="Top 2-3 growth catalysts and whether it's a buy for growth investors.",
    agent=growth_hacker
)

news_headlines = fetch_news(stock)
sentiment_task = Task(
    description=f"Given these recent news headlines about {stock}:\n{news_headlines}\n\nAnalyze the overall sentiment and how it might affect investor perception.",
    expected_output="Short summary of public sentiment and potential impact.",
    agent=sentiment_analyst
)
# Summary task
summary_llm = ChatOpenAI(model="gpt-4", api_key=OPENAI_API_KEY)

def summarize_insights(risks, value, growth, sentiment):
    summary_prompt = f"""
    Based on the following analyses for the stock {stock}:

    - Risks:
    {risks}

    - Valuation:
    {value}

    - Growth:
    {growth}

    - Sentiment:
    {sentiment}

    Provide a short summary (2-3 sentences) with an investment recommendation.
    """
    return summary_llm.invoke(summary_prompt).content

crew = Crew(
    agents=[risk_analyst, value_investor, growth_hacker, sentiment_analyst],
    tasks=[risk_task, value_task, growth_task, sentiment_task],
    verbose=True
)

if __name__ == "__main__":
    results = crew.kickoff()
    if hasattr(results, 'tasks_output') and isinstance(results.tasks_output, list) and len(results.tasks_output) == 4:
        summary = summarize_insights(results.tasks_output[0], results.tasks_output[1], results.tasks_output[2], results.tasks_output[3])
        print("\n\n=== Final Summary and Recommendation ===")
        print(summary)
    else:
        print("Unexpected results format:", results)
