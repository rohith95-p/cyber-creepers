import pandas as pd

class ClientComparator:
    def __init__(self):
        pass

    def compare_clients(self, client_data_list: list) -> dict:
        """
        Compares multiple clients side-by-side.
        Expects a list of dictionaries with structure:
        {"client_id": "X", "sharpe": 1.2, "cvar": -0.05, "aum": 500000}
        """
        if not client_data_list:
            return {}
            
        df = pd.DataFrame(client_data_list)
        df.set_index('client_id', inplace=True)
        
        # Rank by Sharpe (Higher is better)
        df['sharpe_rank'] = df['sharpe'].rank(ascending=False)
        
        # Rank by Risk (CVaR - closer to 0 is better)
        df['risk_rank'] = df['cvar'].rank(ascending=False)
        
        # Peer group averages
        peer_avg_sharpe = df['sharpe'].mean()
        peer_avg_risk = df['cvar'].mean()
        
        comparison_results = {
            "client_rankings": df.to_dict(orient="index"),
            "peer_group_averages": {
                "avg_sharpe": round(peer_avg_sharpe, 3),
                "avg_cvar": round(peer_avg_risk, 3)
            },
            "top_performer": df['sharpe'].idxmax(),
            "safest_portfolio": df['cvar'].idxmax()
        }
        
        return comparison_results
        
    def generate_chart_data(self, df: pd.DataFrame) -> dict:
        """Helper to output data formatted for Plotly in app.py"""
        return {
            "x": df.index.tolist(),
            "y_sharpe": df['sharpe'].tolist(),
            "y_cvar": df['cvar'].tolist()
        }
