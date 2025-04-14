import sys
from langchain_openai import ChatOpenAI
from tools.news_sentiment import fetch_news
from config import LLM_MODEL
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_risk(stock):
    try:
        logger.info(f"Starting risk analysis for {stock}")
        prompt = f"""Analyze {stock} risks in 3-4 bullet points covering:
        - Financial risks
        - Market risks
        - Regulatory risks
        Keep it concise.
        
        At the end, provide a risk score from 1-10 where:
        - 1-3: Low risk
        - 4-6: Moderate risk
        - 7-10: High risk
        
        Format your response as:
        ANALYSIS: [your analysis]
        SCORE: [number from 1-10]"""
        
        response = LLM_MODEL.invoke(prompt)
        logger.info("Risk analysis completed")
        return response.content
    except Exception as e:
        logger.error(f"Error in risk analysis: {str(e)}")
        raise

def analyze_value(stock):
    try:
        logger.info(f"Starting value analysis for {stock}")
        prompt = f"""Evaluate {stock} valuation in 3-4 bullet points covering:
        - Current valuation metrics
        - Historical valuation
        - Industry comparison
        Keep it concise.
        
        At the end, provide a value score from 1-10 where:
        - 1-3: Overvalued
        - 4-6: Fairly valued
        - 7-10: Undervalued
        
        Format your response as:
        ANALYSIS: [your analysis]
        SCORE: [number from 1-10]"""
        
        response = LLM_MODEL.invoke(prompt)
        logger.info("Value analysis completed")
        return response.content
    except Exception as e:
        logger.error(f"Error in value analysis: {str(e)}")
        raise

def analyze_growth(stock):
    try:
        logger.info(f"Starting growth analysis for {stock}")
        prompt = f"""Analyze {stock} growth potential in 3-4 bullet points covering:
        - Revenue growth
        - Market opportunities
        - Product pipeline
        Keep it concise.
        
        At the end, provide a growth score from 1-10 where:
        - 1-3: Low growth potential
        - 4-6: Moderate growth potential
        - 7-10: High growth potential
        
        Format your response as:
        ANALYSIS: [your analysis]
        SCORE: [number from 1-10]"""
        
        response = LLM_MODEL.invoke(prompt)
        logger.info("Growth analysis completed")
        return response.content
    except Exception as e:
        logger.error(f"Error in growth analysis: {str(e)}")
        raise

def analyze_sentiment(stock):
    try:
        logger.info(f"Starting sentiment analysis for {stock}")
        # First get the news
        news_items = fetch_news(stock)
        news_text = "\n".join([item['headline'] for item in news_items])
        
        prompt = f"""Analyze sentiment for {stock} based on these headlines:
        {news_text}
        
        Provide a 2-3 sentence summary of:
        - Overall sentiment
        - Key themes
        - Investor impact
        
        At the end, provide a sentiment score from 1-10 where:
        - 1-3: Negative sentiment
        - 4-6: Neutral sentiment
        - 7-10: Positive sentiment
        
        Format your response as:
        ANALYSIS: [your analysis]
        SCORE: [number from 1-10]"""
        
        response = LLM_MODEL.invoke(prompt)
        logger.info("Sentiment analysis completed")
        return response.content, news_items
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise

def run_analysis(stock, progress_callback=None):
    logger.info(f"Starting analysis for stock: {stock}")
    
    try:
        # Risk Analysis
        logger.info("Starting risk analysis...")
        if progress_callback:
            progress_callback("current_section", "risk")
        risk_result = analyze_risk(stock)
        if progress_callback:
            progress_callback("risk", risk_result)
        
        # Value Analysis
        logger.info("Starting value analysis...")
        if progress_callback:
            progress_callback("current_section", "value")
        value_result = analyze_value(stock)
        if progress_callback:
            progress_callback("value", value_result)
        
        # Growth Analysis
        logger.info("Starting growth analysis...")
        if progress_callback:
            progress_callback("current_section", "growth")
        growth_result = analyze_growth(stock)
        if progress_callback:
            progress_callback("growth", growth_result)
        
        # Sentiment Analysis
        logger.info("Starting sentiment analysis...")
        if progress_callback:
            progress_callback("current_section", "sentiment")
        sentiment_result, news_items = analyze_sentiment(stock)
        if progress_callback:
            progress_callback("sentiment", sentiment_result)
            progress_callback("news", news_items)
        
        return risk_result, value_result, growth_result, sentiment_result, news_items
        
    except Exception as e:
        logger.error(f"Error in run_analysis: {str(e)}")
        raise

def summarize_insights(stock, risks, value, growth, sentiment):
    logger.info("Starting summary generation...")
    summary_prompt = f"""
    Based on these analyses for {stock}:

    Risks: {risks}
    Value: {value}
    Growth: {growth}
    Sentiment: {sentiment}

    Provide a 2-3 sentence investment recommendation.
    """
    try:
        logger.info("Generating summary...")
        result = LLM_MODEL.invoke(summary_prompt).content
        logger.info("Summary generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error in summarize_insights: {str(e)}")
        raise

if __name__ == "__main__":
    stock = sys.argv[1] if len(sys.argv) > 1 else "NVIDIA"
    results = run_analysis(stock)
    if results:
        risks, value, growth, sentiment, news = results
        summary = summarize_insights(stock, risks, value, growth, sentiment)
        print("\n\n=== Final Summary and Recommendation ===")
        print(summary)
    else:
        print("Analysis failed to generate results")


