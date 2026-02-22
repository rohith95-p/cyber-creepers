import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Simulates a database for Supervised Fine-Tuning dataset collection
DB_PATH = "data/approved_reports.json"

def init_db():
    """Ensure the target directory and JSON file exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)

def save_approved_report(state: Dict[str, Any]):
    """Save the full context and final report to disk."""
    try:
        init_db()
        try:
            with open(DB_PATH, "r") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
            
        record = {
            "timestamp": datetime.now().isoformat(),
            "client_id": state.get("client_id"),
            "profile": state.get("client_profile"),
            "portfolio": state.get("portfolio_assets"),
            "risk_metrics": state.get("risk_metrics"),
            "news": state.get("news_summary"),
            "fundamentals": state.get("fundamentals_summary"),
            "macro": state.get("macro_summary"),
            "buffett_raw": state.get("buffett_analysis"),
            "graham_raw": state.get("graham_analysis"),
            "growth_raw": state.get("cathie_wood_analysis"),
            "final_report": state.get("final_report")
        }
        
        data.append(record)
        
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)
            
        logger.info(f"Successfully saved approved report for {state.get('client_id')} to SFT database.")
        
    except Exception as e:
        logger.error(f"Failed to save report to DB: {e}")
