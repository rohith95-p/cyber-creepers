from typing import Any, Dict
from src.utils.feedback_db import save_approved_report
import logging

logger = logging.getLogger(__name__)

def node_save_draft(state: dict[str, Any]) -> dict[str, Any]:
    """Finalizes the report and sets the compliance status."""
    print("--- SAVING REPORT TO CRM: ✅ APPROVED ---")
    
    # This sends the final success signal back to main.py    
    # Save to our local feedback DB for future fine-tuning
    save_approved_report(state)
    
    return {"compliance_status": "Draft Prepared. Awaiting Human-in-the-loop Approval."}