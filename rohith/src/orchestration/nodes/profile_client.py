import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Mock CRM Database for Client Profiles
MOCK_CLIENT_DB = {
    "PUNEETH_001": {
        "age": 45,
        "risk_tolerance": "moderate",
        "investment_horizon_years": 15,
        "time_horizon_years": 15,
        "primary_goal": "Retirement and wealth preservation",
        "goal_amount_usd": 2_000_000,
        "current_portfolio_value_usd": 250_000,
        "liquidity_needs": "Low",
        "experience": "Intermediate, comfortable with standard equities and bonds."
    },
    "AGGRESSIVE_002": {
        "age": 28,
        "risk_tolerance": "high",
        "investment_horizon_years": 30,
        "time_horizon_years": 30,
        "primary_goal": "Aggressive growth, maximizing capital appreciation",
        "goal_amount_usd": 5_000_000,
        "current_portfolio_value_usd": 75_000,
        "liquidity_needs": "Low",
        "experience": "Advanced, understands volatility and actively trades."
    },
    "CONSERVATIVE_003": {
        "age": 68,
        "risk_tolerance": "low",
        "investment_horizon_years": 5,
        "time_horizon_years": 5,
        "primary_goal": "Income generation and capital preservation",
        "goal_amount_usd": 600_000,
        "current_portfolio_value_usd": 500_000,
        "liquidity_needs": "High",
        "experience": "Low, prefers safety over high returns."
    }
}

def node_profile_client(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates retrieving a detailed client profile from a CRM.
    """
    client_id = state.get("client_id", "")
    client_data = state.get("client_data", {})
    
    logger.info(f"Retrieving profile for client: {client_id}")
    
    # Fetch from mock DB for deep history, but OVERRIDE with live data from state
    base_profile = MOCK_CLIENT_DB.get(client_id, {
        "age": 50,
        "risk_tolerance": "moderate",
        "investment_horizon_years": 10,
        "primary_goal": "General wealth building",
        "liquidity_needs": "Moderate",
        "experience": "Average Retail Investor"
    })
    
    # Merge with live data passed from api.py
    profile = {**base_profile}
    if client_data:
        profile["name"] = client_data.get("name", "Unknown Client")
        profile["risk_tolerance"] = client_data.get("risk_tolerance", profile["risk_tolerance"])
        profile["current_portfolio_value_usd"] = client_data.get("portfolio_value", profile["current_portfolio_value_usd"])
        profile["email"] = client_data.get("email", "")
    
    return {"client_profile": profile}
