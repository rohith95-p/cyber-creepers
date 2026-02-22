import logging
import os
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.error_handler import safe_llm_invoke

logger = logging.getLogger(__name__)

CACHE_DIR = Path("./agent_cache")
CACHE_DIR.mkdir(exist_ok=True)

def _get_cached_or_compute(key_prefix: str, client_id: str, data: dict, compute_fn):
    """Smart cache: return saved result if under 24 hours old to save API quota."""
    cache_key = hashlib.sha256(
        f"{key_prefix}:{client_id}:{json.dumps(data, sort_keys=True)}".encode()
    ).hexdigest()
    
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                cached = json.load(f)
                cached_time = datetime.fromisoformat(cached["timestamp"])
                if datetime.now() - cached_time < timedelta(hours=24):
                    logger.info(f"CACHE HIT: {key_prefix} (0 API Calls)")
                    return cached["result"]
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            
    # Compute fresh
    logger.info(f"CACHE MISS: Computing fresh {key_prefix}...")
    result = compute_fn()
    
    # Save cache
    try:
        with open(cache_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "result": result
            }, f)
    except Exception as e:
        logger.warning(f"Cache write error: {e}")
        
    return result

def node_persona_ensemble(state: dict[str, Any]) -> dict[str, Any]:
    """Generates 3 distinct persona analyses in a SINGLE batched API call to save 66% on quota."""
    client_id = state.get("client_id", "Unknown")
    logger.info(f"node_persona_ensemble: batch analyzing portfolio for {client_id}")
    
    portfolio = state.get("portfolio_assets", [])
    fundamentals = state.get("fundamentals_summary", {})
    news = state.get("news_summary", {})
    macro = state.get("macro_summary", "")

    # Data payload for cache signature
    payload = {
        "portfolio": portfolio,
        "fundamentals": fundamentals,
        "news": news,
        "macro": macro
    }

    def _call_llm():
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", 
                temperature=0.3,
                google_api_key=api_key,
                max_retries=3
            )
            
            prompt = f"""
            Analyze this portfolio from THREE distinct perspectives:
            
            PORTFOLIO DATA:
            Holdings: {portfolio}
            Fundamentals: {fundamentals}
            News/Catalysts: {news}
            Macro Context: {macro}
            
            Required Output format MUST be a valid JSON object with exactly these three keys:
            {{
                "buffett_analysis": "Write 2 paragraphs as Warren Buffett focusing on economic moats, value, and holding forever...",
                "graham_analysis": "Write 2 paragraphs as Benjamin Graham strictly analyzing P/E, debt, and margin of safety...",
                "growth_analysis": "Write 2 paragraphs as Cathie Wood looking at disruption, AI tailwinds, and hyper-growth potential..."
            }}
            
            Return ONLY the valid JSON block without markdown formatting or code ticks.
            """
            
            response = safe_llm_invoke(llm, prompt)
            
            # Clean standard markdown ticks if Gemini adds them
            clean_text = response.content.strip()
            if clean_text.startswith("
```
json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("
```
"):
                clean_text = clean_text[:-3]
                
            return json.loads(clean_text)
            
        except Exception as e:
            logger.error(f"Ensemble Persona Error: {e}")
            return {
                "buffett_analysis": "Buffett batch analysis failed.",
                "graham_analysis": "Graham batch analysis failed.",
                "growth_analysis": "Growth batch analysis failed."
            }

    # Call the smart cache
    results = _get_cached_or_compute("ensemble", client_id, payload, _call_llm)
    
    return {
        "buffett_analysis": results.get("buffett_analysis", "Missing"),
        "graham_analysis": results.get("graham_analysis", "Missing"),
        "cathie_wood_analysis": results.get("growth_analysis", "Missing")
    }
