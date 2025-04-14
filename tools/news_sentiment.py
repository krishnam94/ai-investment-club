import requests
from config import SERPAPI_KEY, LLM_MODEL
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def analyze_sentiment(headline):
    prompt = PromptTemplate(
        input_variables=["headline"],
        template="Analyze the sentiment of this news headline about a stock. Return only one of: POSITIVE, NEGATIVE, or NEUTRAL.\nHeadline: {headline}"
    )
    chain = LLMChain(llm=LLM_MODEL, prompt=prompt)
    result = chain.run(headline=headline)
    return result.strip()

def fetch_news(stock):
    url = "https://serpapi.com/search"
    params = {
        "q": f"{stock} stock news",
        "tbm": "nws",
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    news_items = []
    for item in data.get("news_results", [])[:5]:
        headline = item['title']
        sentiment = analyze_sentiment(headline)
        news_items.append({
            'headline': headline,
            'sentiment': sentiment,
            'source': item.get('source', 'Unknown'),
            'date': item.get('date', 'Unknown')
        })
    
    return news_items