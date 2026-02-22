"""
AgentState — shared state schema for the wealth management LangGraph pipeline.

Every node reads from and writes to this TypedDict as it flows through
the graph: fetch_crm → fetch_market → analyze_risk → generate_report → save_draft.
"""

from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    """Shared state flowing through the supervisor graph.

    Fields
    ------
    client_id : str
        Salesforce Account / Contact identifier supplied at pipeline entry.
    portfolio_assets : list[dict]
        Client holdings retrieved from the CRM.
    market_data : dict
        Historical OHLCV data keyed by ticker.
    risk_metrics : dict
        Quantitative risk outputs.
    final_report : str
        Structured Markdown wealth-management report.
    compliance_status : str
        Regulatory compliance status.
    client_profile : dict
        Consolidated client details and goals.
    news_summary : dict[str, str]
        Key news headlines and sentiment per ticker.
    fundamentals_summary : dict[str, str]
        Core financial metrics and ratios.
    macro_summary : str
        Global economic outlook summary.
    buffett_analysis : str
        Value-based persona analysis.
    graham_analysis : str
        Defensive persona analysis.
    cathie_wood_analysis : str
        Growth-oriented persona analysis.
    goal_planning_analysis : str
        Analysis of progress toward client financial goals.
    """

    client_id: str
    portfolio_assets: list[dict]
    market_data: dict
    risk_metrics: dict
    final_report: str
    compliance_status: str
    client_profile: dict
    news_summary: dict[str, str]
    fundamentals_summary: dict[str, str]
    macro_summary: str
    buffett_analysis: str
    graham_analysis: str
    cathie_wood_analysis: str
    goal_planning_analysis: str
