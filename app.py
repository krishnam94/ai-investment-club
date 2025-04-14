import streamlit as st
from main import run_analysis, summarize_insights
import os
import traceback
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (for local development)
load_dotenv()

# Function to get API keys from various sources
def get_api_keys():
    # Try to get keys from environment variables first (local development)
    openai_key = os.getenv("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    # If not found in environment, try Streamlit secrets (cloud deployment)
    if not openai_key or not serpapi_key:
        try:
            openai_key = st.secrets["OPENAI_API_KEY"]
            serpapi_key = st.secrets["SERPAPI_KEY"]
        except:
            pass
    
    return openai_key, serpapi_key

# Get API keys
openai_key, serpapi_key = get_api_keys()

# Check if we have both API keys
if not openai_key or not serpapi_key:
    st.error("""
    ⚠️ API keys not found! Please add them in one of these ways:
    
    For local development:
    1. Create a .env file in the project root
    2. Add your API keys:
        OPENAI_API_KEY=your-openai-api-key
        SERPAPI_KEY=your-serpapi-key
    
    For Streamlit Cloud deployment:
    1. Go to your app's settings
    2. Click on "Secrets"
    3. Add these secrets:
        OPENAI_API_KEY = "your-openai-api-key"
        SERPAPI_KEY = "your-serpapi-key"
    """)
    st.stop()

# Set environment variables
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["SERPAPI_KEY"] = serpapi_key

st.set_page_config(page_title="AI Investment Club", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stExpander {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
    }
    .stMarkdown {
        font-size: 1.1rem;
    }
    .stButton>button {
        width: 200px;
        margin: 0 auto;
        display: block;
    }
    .score-container {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .score-bar {
        flex-grow: 1;
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin: 0 10px;
    }
    .score-fill {
        height: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
    }
    .score-text {
        font-weight: bold;
        min-width: 30px;
        text-align: center;
    }
    .loading-dots {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin: 20px 0;
    }
    .dot {
        animation: bounce 1.4s infinite;
        margin: 0 5px;
    }
    .dot:nth-child(1) { animation-delay: 0s; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
    }
    .analyzing-section {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 5px 0;
    }
    .analyzing-icon {
        margin-right: 10px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI Investment Club")
st.markdown("Get investment insights from AI-powered analyst personas.")

# Initialize session state for results
if 'results' not in st.session_state:
    st.session_state.results = {
        'risk': None,
        'value': None,
        'growth': None,
        'sentiment': None,
        'news': None,
        'summary': None
    }
    st.session_state.analysis_started = False
    st.session_state.analysis_complete = False
    st.session_state.current_section = None

def update_progress(section, result):
    logger.info(f"Updating progress for {section}")
    st.session_state.results[section] = result
    st.session_state.current_section = None

def extract_score(text):
    try:
        score_line = text.split('SCORE:')[-1].strip()
        score = int(score_line.split()[0])
        return min(max(score, 1), 10)  # Ensure score is between 1 and 10
    except:
        return 5  # Default score if parsing fails

def display_score(score, label):
    st.markdown(f"""
    <div class="score-container">
        <span>{label}</span>
        <div class="score-bar">
            <div class="score-fill" style="width: {score * 10}%"></div>
        </div>
        <span class="score-text">{score}/10</span>
    </div>
    """, unsafe_allow_html=True)

# Input section
st.markdown("### 🔍 Enter Stock Symbol")
stock = st.text_input("Stock Symbol (e.g. AAPL, TSLA, MSFT):", value="AAPL", label_visibility="collapsed")

# Reset session state if stock symbol changes
if 'current_stock' not in st.session_state:
    st.session_state.current_stock = stock
elif st.session_state.current_stock != stock:
    st.session_state.current_stock = stock
    st.session_state.results = {
        'risk': None,
        'value': None,
        'growth': None,
        'sentiment': None,
        'news': None,
        'summary': None
    }
    st.session_state.analysis_started = False
    st.session_state.analysis_complete = False
    st.session_state.current_section = None

analyze_clicked = st.button("Analyze")

# Display loading animation
if st.session_state.analysis_started and not st.session_state.analysis_complete:
    st.markdown("""
    <div class="loading-dots">
        <span>Analyzing</span>
        <span class="dot">.</span>
        <span class="dot">.</span>
        <span class="dot">.</span>
    </div>
    """, unsafe_allow_html=True)

# Display analysis progress
if st.session_state.analysis_started and not st.session_state.analysis_complete:
    st.markdown("### 🔄 Analysis Progress")
    
    sections = [
        ('risk', '🔍 Risk Analysis'),
        ('value', '💰 Value Analysis'),
        ('growth', '📈 Growth Analysis'),
        ('sentiment', '😊 Sentiment Analysis')
    ]
    
    for section_id, section_name in sections:
        status = "✅" if st.session_state.results[section_id] else "⏳"
        if st.session_state.current_section == section_id:
            status = "🔄"
            st.markdown(f"""
            <div class="analyzing-section">
                <span class="analyzing-icon">🔄</span>
                <span>Currently analyzing: {section_name}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"{status} {section_name}")

if analyze_clicked and not st.session_state.analysis_complete:
    # Clear previous results
    st.session_state.results = {
        'risk': None,
        'value': None,
        'growth': None,
        'sentiment': None,
        'news': None,
        'summary': None
    }
    st.session_state.analysis_started = True
    st.session_state.analysis_complete = False
    
    try:
        # Run analysis with progress callback
        results = run_analysis(stock, progress_callback=update_progress)
        
        if results is None:
            logger.error("Analysis failed to generate results")
            st.error("Analysis failed to generate results. Please try again.")
        elif not isinstance(results, tuple) or len(results) != 5:
            logger.error(f"Unexpected results format. Got {type(results)} with length {len(results) if hasattr(results, '__len__') else 'N/A'}")
            st.error(f"Unexpected results format. Got {type(results)} with length {len(results) if hasattr(results, '__len__') else 'N/A'}")
        else:
            st.session_state.analysis_complete = True
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}")
        st.error(f"Something went wrong: {str(e)}")
        st.error("Full error details:")
        st.code(traceback.format_exc())
        st.session_state.analysis_complete = True

# Display results in a grid layout
if st.session_state.results['risk'] or st.session_state.results['value'] or st.session_state.results['growth']:
    # Final Summary at the top
    if all(st.session_state.results[section] for section in ['risk', 'value', 'growth', 'sentiment']):
        st.markdown("### 💡 Investment Recommendation")
        try:
            logger.info("Generating summary...")
            summary = summarize_insights(
                stock,
                st.session_state.results['risk'],
                st.session_state.results['value'],
                st.session_state.results['growth'],
                st.session_state.results['sentiment']
            )
            logger.info("Summary generated successfully")
            st.success(summary)
        except Exception as summary_error:
            logger.error(f"Error generating summary: {str(summary_error)}")
            st.error(f"Error generating summary: {str(summary_error)}")
            st.error("Full error details:")
            st.code(traceback.format_exc())
    
    st.markdown("### 📈 Analysis Results")
    
    # Create three columns for risk, value, and growth analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.results['risk']:
            with st.expander("🔍 Risk Analysis", expanded=True):
                st.markdown(f"**{stock} Risk Assessment**")
                risk_text = st.session_state.results['risk'].strip() if isinstance(st.session_state.results['risk'], str) else str(st.session_state.results['risk'])
                risk_score = extract_score(risk_text)
                display_score(risk_score, "Risk Level")
                st.markdown(f"> {risk_text.split('ANALYSIS:')[-1].split('SCORE:')[0].strip()}")
    
    with col2:
        if st.session_state.results['value']:
            with st.expander("💰 Value Analysis", expanded=True):
                st.markdown(f"**{stock} Valuation**")
                value_text = st.session_state.results['value'].strip() if isinstance(st.session_state.results['value'], str) else str(st.session_state.results['value'])
                value_score = extract_score(value_text)
                display_score(value_score, "Value Rating")
                st.markdown(f"> {value_text.split('ANALYSIS:')[-1].split('SCORE:')[0].strip()}")
    
    with col3:
        if st.session_state.results['growth']:
            with st.expander("📈 Growth Analysis", expanded=True):
                st.markdown(f"**{stock} Growth Potential**")
                growth_text = st.session_state.results['growth'].strip() if isinstance(st.session_state.results['growth'], str) else str(st.session_state.results['growth'])
                growth_score = extract_score(growth_text)
                display_score(growth_score, "Growth Potential")
                st.markdown(f"> {growth_text.split('ANALYSIS:')[-1].split('SCORE:')[0].strip()}")

# News and Sentiment section
if st.session_state.results['news'] or st.session_state.results['sentiment']:
    st.markdown("### 📰 News & Sentiment")
    
    # Create two columns for news and sentiment
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.results['news']:
            with st.expander("📰 Latest News Headlines", expanded=True):
                for item in st.session_state.results['news']:
                    sentiment_emoji = {
                        'POSITIVE': '🟢',
                        'NEGATIVE': '🔴',
                        'NEUTRAL': '⚪'
                    }.get(item['sentiment'], '⚪')
                    
                    st.markdown(f"""
                    {sentiment_emoji} **{item['headline']}**  
                    *{item['source']} - {item['date']}*
                    """)
    
    with col2:
        if st.session_state.results['sentiment']:
            with st.expander("😊 Sentiment Analysis", expanded=True):
                st.markdown(f"**{stock} Market Sentiment**")
                sentiment_text = st.session_state.results['sentiment'].strip() if isinstance(st.session_state.results['sentiment'], str) else str(st.session_state.results['sentiment'])
                sentiment_score = extract_score(sentiment_text)
                display_score(sentiment_score, "Sentiment")
                st.markdown(f"> {sentiment_text.split('ANALYSIS:')[-1].split('SCORE:')[0].strip()}")