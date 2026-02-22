import pytest
import numpy as np
from src.orchestration.nodes.analyze_risk import node_analyze_risk

def test_empty_market_data():
    state = {"market_data": {}}
    result = node_analyze_risk(state)
    assert "risk_metrics" in result
    assert result["risk_metrics"] == {}

def test_mock_risk_calculation():
    # Provide synthetic market data
    mock_market_data = {
        "AAPL": [{"close": 100}, {"close": 105}, {"close": 110}],
        "MSFT": [{"close": 200}, {"close": 190}, {"close": 195}]
    }
    state = {"market_data": mock_market_data}
    
    result = node_analyze_risk(state)
    
    assert "risk_metrics" in result
    metrics = result["risk_metrics"]
    
    assert "cvar_95" in metrics
    assert "max_drawdown" in metrics
    assert "sharpe_ratio" in metrics
    
    # Max drawdown could be exactly 0 if simulated paths don't dip below start value in the mock
    assert metrics["max_drawdown"] <= 0
    assert isinstance(metrics["sharpe_ratio"], float)

def test_single_data_point_handling():
    # Should not crash on single data point (cannot calculate returns)
    mock_market_data = {
        "AAPL": [{"close": 100}]
    }
    state = {"market_data": mock_market_data}
    result = node_analyze_risk(state)
    
    metrics = result["risk_metrics"]
    assert metrics["cvar_95"] == 0.0
