import logging
import os
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from src.utils.error_handler import safe_llm_invoke
from src.utils.smart_cache import get_cached_or_compute
from src.utils.llm_provider import get_llm

logger = logging.getLogger(__name__)

# Mock News Feed (In a real system, this would call a News API like Alpaca or Finnhub)
MOCK_NEWS = {
    "AAPL": "Apple releases new AI-powered hardware, receiving mixed reviews. Supply chain issues persist in Asia. Analysts maintain a cautious but positive outlook.",
    "MSFT": "Microsoft announces major cloud contract with US Government. Azure growth beats expectations. AI integration across Office products drives subscription revenue.",
    "GOOGL": "Google faces new antitrust scrutiny in the EU regarding advertising technology. Search dominance remains strong, but AI competition from startups is increasing.",
    "AMZN": "Amazon Web Services (AWS) announces new custom AI chips. Retail division shows strong holiday sales. Logistics costs stabilized.",
    "BND": "Bond markets steady after Federal Reserve signals a pause in interest rate hikes. Yields remain attractive for conservative investors."
}

def node_summarize_news(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates fetching and summarizing recent news for each asset in the portfolio.
    Uses a smaller, faster LLM (Gemini 1.5 Flash) for efficient text processing.
    """
    logger.info("Summarizing asset news...")
    portfolio = state.get("portfolio_assets", [])
    news_summary = {}

    if not portfolio:
        return {"news_summary": {}}

    try:
        # Use Gemini 1.5 Flash for fast summarization (tool usage pattern)
        llm = get_llm(temperature=0.2)
        
        prompt_template = PromptTemplate.from_template(
            "You are a financial news summarizer. Summarize the following news headlines into one concise sentence focusing on sentiment (Bullish/Bearish/Neutral) and the key driver.\n\nNews for {ticker}: {news_text}"
        )
        chain = prompt_template | llm

        for asset in portfolio:
            ticker = asset.get("ticker")
            if ticker:
                # 1. Fetch
                raw_news = MOCK_NEWS.get(ticker, f"No significant news found for {ticker} today.")
                
                # 2. Summarize via LLM (Cached)
                def _call_news_llm():
                    return safe_llm_invoke(chain, {"ticker": ticker, "news_text": raw_news}).content.strip()
                    
                client_id = state.get("client_id", "Unknown")
                payload = {"ticker": ticker, "news": raw_news}
                news_summary[ticker] = get_cached_or_compute(f"news_{ticker}", client_id, payload, _call_news_llm)
                
    except Exception as e:
        logger.error(f"Error in news summarizer: {e}")
        # Graceful degradation: return raw mock news if LLM fails
        for asset in portfolio:
            ticker = asset.get("ticker", "Unknown")
            news_summary[ticker] = MOCK_NEWS.get(ticker, "Data unavailable.")

    return {"news_summary": news_summary}
