import streamlit as st
from main import run_analysis
import os
import traceback

# Debug: show whether API keys are detected
# if os.getenv("OPENAI_API_KEY") and os.getenv("SERPAPI_KEY"):
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     SERPAPI_KEY = os.getenv("SERPAPI_KEY")
# else:
#     import streamlit as st
#     OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
#     SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
# st.sidebar.title("🔐 API Key Check")
# st.sidebar.write("OpenAI Key Found:", bool(OPENAI_API_KEY))
# st.sidebar.write("SerpAPI Key Found:", bool(SERPAPI_KEY))

st.set_page_config(page_title="AI Investment Club", layout="wide")

st.markdown("""
# 💼 AI Investment Club

Welcome to the AI-powered investment advisor. Enter a stock ticker to get a deep-dive analysis from four specialized agents:
- Risk Analyst 🔍
- Value Investor 💰
- Growth Hacker 🚀
- Sentiment Analyst (with latest news) 📰

""")



with st.container():
    stock = st.text_input("🔎 Enter stock symbol (e.g. AAPL, TSLA, MSFT):", value="AAPL")
    run_button = st.button("📈 Run Analysis")

if run_button:
    with st.spinner("Thinking like an investment club of analysts..."):
        try:
            import traceback
            st.info(f"Starting analysis for: `{stock}`")
            results = run_analysis(stock)
            if results:
                try:
                    risks, value, growth, sentiment = results
                    st.markdown("---")
                    st.header("🧠 Agent Perspectives")

                    # Highlight sentiment keywords
                    st.markdown("### 📰 Sentiment Analyst")
                    highlighted_sentiment = str(sentiment).replace("positive", "**🟢 positive**").replace("negative", "**🔴 negative**").replace("neutral", "**🟡 neutral**")
                    with st.expander("Sentiment Summary"):
                        st.markdown(highlighted_sentiment)

                    # Display fetched news if available
                    if hasattr(results, 'news') and results.news:
                        with st.expander("📰 Recent News Headlines"):
                            for line in results.news.split(""):
                                st.markdown(f"- {line.strip()}")

                    

                    with st.expander("💼 Risk Analyst"):
                        st.markdown(f"> {risks.strip() if isinstance(risks, str) else str(risks)}")

                    with st.expander("📉 Value Investor"):
                        st.markdown(f"> {value.strip() if isinstance(value, str) else str(value)}")

                    with st.expander("🚀 Growth Hacker"):
                        st.markdown(f"> {growth.strip() if isinstance(growth, str) else str(growth)}")

                    
                    
                except Exception as unpack_error:
                    st.error(f"❌ Error processing results: {str(unpack_error)}")
                    with st.expander("Show traceback"):
                        st.code(traceback.format_exc())
            else:
                st.error("⚠️ Failed to generate analysis. Please check your API keys or try another stock.")
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
            with st.expander("Show traceback"):
                st.code(traceback.format_exc())
