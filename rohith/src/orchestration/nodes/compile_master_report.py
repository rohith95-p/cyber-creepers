import logging
import os
from typing import Any
from src.utils.error_handler import safe_llm_invoke
from src.utils.llm_provider import get_llm
from src.utils.smart_cache import get_cached_or_compute

logger = logging.getLogger(__name__)

def compile_master_report(state: dict[str, Any]) -> dict[str, Any]:
    """Synthesize the three distinct persona analyses into a master consensus report."""
    logger.info("compile_master_report: building consensus for client %s", state.get("client_id"))
    print("--- GENERATING REAL AI REPORT (GOOGLE GEMINI) ---")
    
    client_id = state.get("client_id", "Unknown")
    portfolio = state.get("portfolio_assets", [])
    risk = state.get("risk_metrics", {})
    profile = state.get("client_profile", {})
    
    # Retrieve the three persona analyses
    buffett = state.get("buffett_analysis", "Buffett analysis missing.")
    graham = state.get("graham_analysis", "Graham analysis missing.")
    growth = state.get("cathie_wood_analysis", "Growth analysis missing.")

    try:
        def _call_synthesis():
            llm = get_llm(temperature=0.3)
            prompt = (
                f"Profile: {profile}\nPortfolio: {portfolio}\nRisk: {risk}\n"
                f"Buffett: {buffett}\nGraham: {graham}\nGrowth: {growth}\n"
                "Synthesize a professional consensus wealth report in Markdown.\n"
                "You MUST use exactly these major markers:\n"
                "- Write an introductory analysis first.\n"
                "- Use **Key Strengths:** to start the strengths section.\n"
                "- Use **Areas for Consideration:** for risks.\n"
                "- Use **Overall:** to start the final strategic recommendation."
            )
            response = safe_llm_invoke(llm, prompt)
            return response.content

        payload = {
            "profile": profile, "portfolio": portfolio, "risk": risk,
            "buffett": buffett, "graham": graham, "growth": growth
        }
        
        # Use our new globally synchronized safe cache wrapper
        final_report = get_cached_or_compute("master_report", client_id, payload, _call_synthesis)
        
    except Exception as e:
        logger.error(f"AI Generation Error: {str(e)}")
        final_report = f"AI Generation Error: {str(e)}"

    logger.info("compile_master_report: completed — %d characters", len(final_report))
    return {"final_report": final_report}