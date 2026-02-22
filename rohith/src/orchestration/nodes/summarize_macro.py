import logging
import os
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from src.utils.error_handler import safe_llm_invoke
from src.utils.smart_cache import get_cached_or_compute
from src.utils.llm_provider import get_llm

logger = logging.getLogger(__name__)

# Mock Macro Report (Could come from a weekly PDF, Fed Minutes, or OpenBB)
MOCK_MACRO_TEXT = """
Global macroeconomic conditions remain resilient despite elevated interest rates. 
The Federal Reserve has indicated a potential pivot towards rate cuts in the second half of the year, 
provided inflation continues its downward trajectory towards the 2% target. 
Labor markets remain tight, though wage growth has cooled slightly. 
Geopolitical tensions in the Middle East and Eastern Europe continue to pose supply chain risks, 
particularly for energy and semiconductor sectors.
Consumer spending has slightly slowed, indicating that tighter monetary policy is working its way through the economy.
"""

def node_summarize_macro(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a top-down macroeconomic summarizer agent.
    Takes a large, weekly macro report and condenses it into actionable insights for the portfolio.
    """
    logger.info("Summarizing macro environment...")
    
    try:
        def _call_macro_llm():
            llm = get_llm(temperature=0.1)
            prompt_template = PromptTemplate.from_template(
                "You are a Chief Economist. Summarize the following macroeconomic text into a 3-bullet-point executive summary. Focus on implications for Equity and Fixed Income markets.\n\nMacro Text: {macro_text}"
            )
            chain = prompt_template | llm
            response = safe_llm_invoke(chain, {"macro_text": MOCK_MACRO_TEXT})
            return response.content.strip()

        client_id = state.get("client_id", "Unknown")
        payload = {"macro_text": MOCK_MACRO_TEXT} # Cache strictly by the input text
        macro_summary = get_cached_or_compute("macro", client_id, payload, _call_macro_llm)
        
    except Exception as e:
         logger.error(f"Error in macro summarizer: {e}")
         # Fallback mechanism
         macro_summary = "Macro summary unavailable due to API error. Assume standard volatile market conditions."
         
    return {"macro_summary": macro_summary}
