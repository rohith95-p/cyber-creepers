import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

from src.orchestration.supervisor_graph import app
from src.orchestration.nodes.fetch_crm import fetch_crm

def test_fetch_crm_mock():
    # Test state management
    initial_state = {"client_id": "TEST_001"}
    result = fetch_crm(initial_state)
    assert "portfolio_assets" in result
    assert len(result["portfolio_assets"]) > 0

@patch('src.utils.error_handler.safe_llm_invoke')
@patch('src.orchestration.nodes.fetch_market.yf.Ticker')
@patch('src.orchestration.nodes.summarize_fundamentals.yf.Ticker')
def test_pipeline_missing_client(mock_yf_fundamentals, mock_yfinance, mock_safe_llm):
    """Full pipeline runs with mocks; no API/network needed."""
    mock_response = MagicMock()
    mock_response.content = (
        '{"buffett_analysis": "Hold.", "graham_analysis": "Buy.", "growth_analysis": "Accumulate."}'
    )
    mock_safe_llm.return_value = mock_response

    dates = pd.DatetimeIndex([datetime.now() - timedelta(days=i) for i in range(3)])
    mock_history_df = pd.DataFrame({
        "Close": [150.0, 152.0, 151.0],
        "High": [151.0, 153.0, 152.0],
        "Low": [149.0, 151.0, 150.0],
    }, index=dates)
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = mock_history_df
    mock_ticker.info = {"forwardPE": 15, "trailingPE": 14, "marketCap": 1e12}
    mock_yfinance.return_value = mock_ticker
    mock_yf_fundamentals.return_value = mock_ticker

    initial_state = {
        "client_id": "PUNEETH_001",
        "portfolio_assets": [],
        "market_data": {},
        "risk_metrics": {},
        "final_report": "",
        "compliance_status": "",
        "client_profile": {},
        "news_summary": {},
        "fundamentals_summary": {},
        "macro_summary": "",
        "buffett_analysis": "",
        "graham_analysis": "",
        "cathie_wood_analysis": "",
        "goal_planning_analysis": "",
    }
    final_state = app.invoke(initial_state)
    assert "final_report" in final_state
    assert "compliance_status" in final_state
    assert "Draft" in final_state["compliance_status"] or "Approved" in final_state["compliance_status"]

def test_pipeline_graph_structure():
    # Verify nodes and edges compile
    assert app is not None
