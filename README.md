# 📊 AI Investment Club

**AI Investment Club** is a multi-agent LLM-powered app that simulates a team of financial analysts evaluating a stock from multiple perspectives — risk, value, growth, and sentiment — and then combines their views into a concise investment recommendation.

Built for demoing autonomous agents and real-time AI-powered financial analysis, the app uses OpenAI, CrewAI, LangChain, and Streamlit for a rich interactive experience.

---

## 🚀 Live Demo

**[▶️ Try the App on Streamlit Cloud](https://your-streamlit-app-url-here)**  
*(replace this link with your deployed app)*

---

## 🤖 What It Does

Given a stock ticker (e.g., `AAPL`, `TSLA`), the app will:
- 🔍 Analyze financial risks via a Risk Analyst agent
- 📉 Evaluate valuation with a Value Investor agent
- 🚀 Assess growth potential using a Growth Hacker agent
- 📰 Summarize public sentiment based on real-time news via a Sentiment Analyst agent
- 💡 Combine all of the above into a 2–3 sentence AI investment recommendation

---

## 🧠 Tech Stack

| Tech / Tool                | Purpose                                               |
|----------------------------|--------------------------------------------------------|
| **Streamlit**              | Interactive web UI                                   |
| **CrewAI**                 | Multi-agent LLM task orchestration                   |
| **LangChain**              | LLM integration, agent memory                        |
| **OpenAI GPT-4**           | Language model powering agents and summarization     |
| **SerpAPI**                | Real-time Google News search for sentiment analysis  |
| **Python**                 | Core language for all logic                          |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ai-investment-club.git
cd ai-investment-club
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Set Your API Keys

You can use a `.env` file locally or Streamlit Cloud's Secrets UI for deployment:

```toml
# .streamlit/secrets.toml or environment variables
OPENAI_API_KEY = "sk-..."
SERPAPI_KEY = "your-serpapi-key"
```

---

## 🛠️ Future Improvements

- [ ] Add visualizations (stock charts, sentiment graphs)
- [ ] Support portfolio recommendations
- [ ] Add memory + persona refinement per agent
- [ ] Deploy with custom domain + analytics

---