import logging
import os
import yfinance as yf
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from src.utils.error_handler import safe_llm_invoke
from src.utils.smart_cache import get_cached_or_compute
from src.utils.llm_provider import get_llm

logger = logging.getLogger(__name__)

def node_summarize_fundamentals(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a fundamental analyst agent.
    Iterates over portfolio_assets, uses yfinance to grab the 'info' dictionary 
    (P/E ratio, market cap, debt-to-equity), and uses an LLM to frame this into a readable summary.
    """
    logger.info("Summarizing asset fundamentals...")
    portfolio = state.get("portfolio_assets", [])
    fundamentals_summary = {}

    if not portfolio:
        return {"fundamentals_summary": {}}

    try:
        # Use Gemini 1.5 Flash for fast summarization
        llm = get_llm(temperature=0.1)
        
        prompt_template = PromptTemplate.from_template(
            "You are a fundamental equity analyst. Review the following key metrics for {ticker} "
            "and provide a concise, maximum 2-sentence summary of the company's valuation and financial health.\n\n"
            "Metrics: {metrics}"
        )
        chain = prompt_template | llm

        for asset in portfolio:
            ticker = asset.get("ticker")
            if ticker:
                try:
                    # 1. Fetch Fundamentals (yfinance info)
                    ticker_obj = yf.Ticker(ticker)
                    info = ticker_obj.info
                    
                    # Extract key metrics cleanly
                    key_metrics = {
                        "Forward P/E": info.get("forwardPE", "N/A"),
                        "Trailing P/E": info.get("trailingPE", "N/A"),
                        "Market Cap": info.get("marketCap", "N/A"),
                        "Debt to Equity": info.get("debtToEquity", "N/A"),
                        "Return on Equity": info.get("returnOnEquity", "N/A"),
                        "Profit Margin": info.get("profitMargins", "N/A")
                    }
                    
                    # 2. Summarize via LLM (Cached)
                    def _call_fund_llm():
                        return safe_llm_invoke(chain, {"ticker": ticker, "metrics": str(key_metrics)}).content.strip()
                        
                    client_id = state.get("client_id", "Unknown")
                    payload = {"ticker": ticker, "metrics": key_metrics}
                    fundamentals_summary[ticker] = get_cached_or_compute(f"fundamentals_{ticker}", client_id, payload, _call_fund_llm)
                    
                except Exception as yf_e:
                    logger.warning(f"Could not fetch fundamentals for {ticker}: {yf_e}")
                    fundamentals_summary[ticker] = "Fundamental data currently unavailable."

    except Exception as e:
        logger.error(f"Error initializing fundamental summarizer: {e}")
        for asset in portfolio:
             ticker = asset.get("ticker", "Unknown")
             fundamentals_summary[ticker] = "API Error: Unable to compute fundamental health."

    return {"fundamentals_summary": fundamentals_summary}
