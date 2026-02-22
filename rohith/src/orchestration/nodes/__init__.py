"""
Pipeline node functions for the wealth management supervisor graph.
"""

from .fetch_crm import fetch_crm
from .fetch_market import node_fetch_market_data
from .analyze_risk import node_analyze_risk
from .save_draft import node_save_draft
from .compile_master_report import compile_master_report
from .persona_ensemble import node_persona_ensemble
from .profile_client import node_profile_client
from .summarize_fundamentals import node_summarize_fundamentals
from .summarize_macro import node_summarize_macro
from .summarize_news import node_summarize_news
from .goal_planner import node_goal_planner

__all__ = [
    "fetch_crm",
    "node_fetch_market_data",
    "node_analyze_risk",
    "node_save_draft",
    "compile_master_report",
    "node_persona_ensemble",
    "node_profile_client",
    "node_summarize_fundamentals",
    "node_summarize_macro",
    "node_summarize_news",
    "node_goal_planner"
]
