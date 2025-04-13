import requests
from config import SERPAPI_KEY

def fetch_news(stock):
    url = "https://serpapi.com/search"
    params = {
        "q": f"{stock} stock news",
        "tbm": "nws",
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    headlines = [item['title'] for item in data.get("news_results", [])[:5]]
    return "\n".join(headlines)