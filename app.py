import streamlit as st
from main import run_analysis, summarize_insights
import os

st.set_page_config(page_title="AI Investment Club", layout="wide")

st.title("📊 AI Investment Club")
st.markdown("Get investment insights from AI-powered analyst personas.")

# Debug: show whether API keys are detected
if os.getenv("OPENAI_API_KEY") and os.getenv("SERPAPI_KEY"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
else:
    import streamlit as st
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
st.sidebar.title("🔐 API Key Check")
st.sidebar.write("OpenAI Key Found:", bool(OPENAI_API_KEY))
st.sidebar.write("SerpAPI Key Found:", bool(SERPAPI_KEY))

stock = st.text_input("Enter stock symbol (e.g. AAPL, TSLA, MSFT):", value="AAPL")

if st.button("Run Analysis"):
    with st.spinner("Running analysis..."):
        try:
            results = run_analysis(stock)
            if results:
                risks, value, growth, sentiment = results

                st.subheader("🔍 Agent Insights")
                st.markdown("---")
                st.expander("💼 Risk Analyst").write(risks)
                st.expander("📉 Value Investor").write(value)
                st.expander("🚀 Growth Hacker").write(growth)
                st.expander("📰 Sentiment Analyst").write(sentiment)

                st.markdown("---")
                st.subheader("💡 Final Investment Summary")
                summary = summarize_insights(stock, risks, value, growth, sentiment)
                st.success(summary)
            else:
                st.error("Failed to generate analysis. Please check your API keys or try another stock.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
