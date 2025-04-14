import streamlit as st
from main import run_analysis, summarize_insights
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

st.title("📊 AI Investment Club")
st.markdown("Get investment insights from AI-powered analyst personas.")

stock = st.text_input("Enter stock symbol (e.g. AAPL, TSLA, MSFT):", value="AAPL")

if st.button("Run Analysis"):
    with st.spinner("Running analysis..."):
        try:
            results = run_analysis(stock)
            if results is None:
                st.error("Analysis failed to generate results. Please try again.")
            elif not isinstance(results, tuple) or len(results) != 5:
                st.error(f"Unexpected results format. Got {type(results)} with length {len(results) if hasattr(results, '__len__') else 'N/A'}")
            else:
                try:
                    risks, value, growth, sentiment, news = results

                    st.subheader("🔍 Agent Insights")
                    st.markdown("---")
                    
                    # Display agent analyses with formatted text
                    with st.expander("💼 Risk Analyst"):
                        st.markdown(f"> {risks.strip() if isinstance(risks, str) else str(risks)}")
                    with st.expander("📉 Value Investor"):
                        st.markdown(f"> {value.strip() if isinstance(value, str) else str(value)}")
                    with st.expander("🚀 Growth Hacker"):
                        st.markdown(f"> {growth.strip() if isinstance(growth, str) else str(growth)}")
                    with st.expander("📰 Sentiment Analyst"):
                        st.markdown(f"> {sentiment.strip() if isinstance(sentiment, str) else str(sentiment)}")

                    st.markdown("---")
                    st.subheader("💡 Final Investment Summary")
                    try:
                        summary = summarize_insights(stock, risks, value, growth, sentiment)
                        st.success(summary)
                    except Exception as summary_error:
                        st.error(f"Error generating summary: {str(summary_error)}")
                        st.error("Full error details:")
                        st.code(traceback.format_exc())

                except Exception as unpack_error:
                    st.error(f"Error processing results: {str(unpack_error)}")
                    st.error("Full error details:")
                    st.code(traceback.format_exc())
                
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.error("Full error details:")
            st.code(traceback.format_exc())