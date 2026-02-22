import logging
from typing import Any

logger = logging.getLogger(__name__)

def fetch_crm(state: dict[str, Any]) -> dict[str, Any]:
    """Retrieve the client's portfolio holdings from the local vault."""
    client_id = state.get("client_id", "Unknown")
    client_data = state.get("client_data", {})
    
    # If we have live client data from the API/Salesforce, use it to scale the mock portfolio
    portfolio_value = client_data.get("portfolio_value", 1000000)
    
    print(f"--- FETCHING PORTFOLIO FOR {client_data.get('name', client_id)} (SCALED VAULT) ---")
    
    # Base portfolio weights
    base_assets = [
        {"ticker": "AAPL", "weight": 0.20, "asset_type": "equity"},
        {"ticker": "MSFT", "weight": 0.25, "asset_type": "equity"},
        {"ticker": "GOOGL", "weight": 0.15, "asset_type": "equity"},
        {"ticker": "AMZN", "weight": 0.10, "asset_type": "equity"},
        {"ticker": "BND", "weight": 0.30, "asset_type": "bond_etf"},
    ]
    
    # Scale quantities based on the client's actual portfolio value for realism
    # Assuming rough prices: AAPL=$180, MSFT=$400, GOOGL=$140, AMZN=$170, BND=$70
    prices = {"AAPL": 180, "MSFT": 400, "GOOGL": 140, "AMZN": 170, "BND": 70}
    
    portfolio_assets = []
    for asset in base_assets:
        ticker = asset["ticker"]
        allocation = portfolio_value * asset["weight"]
        quantity = int(allocation / prices.get(ticker, 100))
        portfolio_assets.append({
            "ticker": ticker,
            "quantity": quantity,
            "asset_type": asset["asset_type"]
        })
    
    return {"portfolio_assets": portfolio_assets}
    
    return {"portfolio_assets": portfolio_assets}