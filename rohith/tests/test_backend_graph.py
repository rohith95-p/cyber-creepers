import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

try:
    from src.orchestration.supervisor_graph import app as graph
except ImportError:
    graph = None

# Patch all LLM calls via safe_llm_invoke (used by persona_ensemble, summarize_*, goal_planner, compile_master_report)
@patch('src.utils.error_handler.safe_llm_invoke')
@patch('src.orchestration.nodes.fetch_market.yf.Ticker')
@patch('src.orchestration.nodes.summarize_fundamentals.yf.Ticker')
def test_full_pipeline_execution(mock_yf_fundamentals, mock_yfinance, mock_safe_llm):
    if graph is None:
        pytest.skip("Graph could not be imported. Check module structure.")

    # 1. Mock Yahoo Finance: history() must return a DataFrame with iterrows() -> date, row with Close/High/Low
    dates = pd.DatetimeIndex([datetime.now() - timedelta(days=i) for i in range(3)])
    mock_history_df = pd.DataFrame({
        "Close": [150.0, 152.0, 151.0],
        "High": [151.0, 153.0, 152.0],
        "Low": [149.0, 151.0, 150.0],
    }, index=dates)
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.history.return_value = mock_history_df
    mock_yfinance.return_value = mock_ticker_instance

    # summarize_fundamentals also uses yf.Ticker for .info
    mock_ticker_instance.info = {"forwardPE": 15, "trailingPE": 14, "marketCap": 1e12, "longBusinessSummary": "Mock."}
    mock_yf_fundamentals.return_value = mock_ticker_instance

    # 2. Mock all LLM calls (persona expects JSON; other nodes use .content as string)
    mock_response = MagicMock()
    mock_response.content = (
        '{"buffett_analysis": "Hold.", "graham_analysis": "Buy.", "growth_analysis": "Accumulate."}'
    )
    mock_safe_llm.return_value = mock_response

    # 3. Initial state; use PUNEETH_001 so profile_client has data
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

    # 4. Run the compiled LangGraph (synchronous invoke)
    final_state = graph.invoke(initial_state)

    # 5. Assertions
    assert final_state.get("portfolio_assets"), "Portfolio data lost in state transition."
    assert "market_data" in final_state
