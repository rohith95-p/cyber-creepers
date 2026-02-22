import yfinance as yf
from src.utils.smart_cache import get_cached_or_compute

def node_fetch_market_data(state):
    print("--- FETCHING REAL MARKET DATA (YAHOO FINANCE) ---")
    portfolio = state.get("portfolio_assets", [])
    client_id = state.get("client_id", "Unknown")
    
    if not portfolio:
        return {"market_data": {}}

    market_data = {}
    try:
        for asset in portfolio:
            ticker = asset.get("ticker")
            if not ticker:
                continue
            
            # Wrap Yahoo Finance in the smart cache with a 12-hour TTL
            # This PREVENTS live intraday prices from fluttering the downstream SHA-256 hashes
            def _fetch_yf():
                stock = yf.Ticker(ticker)
                history = stock.history(period="1y")
                
                prices = []
                for date, row in history.iterrows():
                    prices.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "close": float(row["Close"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"])
                    })
                return prices
            
            # The payload is just the ticker
            market_data[ticker] = get_cached_or_compute(f"market_{ticker}", client_id, {"ticker": ticker}, _fetch_yf, ttl_hours=12)
            
        return {"market_data": market_data}
        
    except Exception as e:
        return {"error": f"Yahoo Finance Error: {str(e)}"}