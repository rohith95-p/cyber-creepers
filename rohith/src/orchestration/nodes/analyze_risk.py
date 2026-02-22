import logging
import numpy as np
import pandas as pd
from typing import Any

logger = logging.getLogger(__name__)

RISK_FREE_RATE = 0.05 / 252  # Daily risk-free rate (annualized 5%)
MONTE_CARLO_PATHS = 10_000
PROJECTION_DAYS = 252         # 1-year projection

def node_analyze_risk(state: dict[str, Any]) -> dict[str, Any]:
    """
    Phase 3 Risk Engine: Advanced analysis including:
    - Real Sharpe & Sortino ratios from market data
    - CVaR (Conditional Value at Risk) at 95% and 99%
    - Max Drawdown
    - Yule's Q for tail dependence between assets
    - 10,000-path Monte Carlo simulation for 1-year portfolio projection
    """
    print("--- ANALYZING PORTFOLIO RISK (Phase 3: Monte Carlo Engine) ---")
    market_data = state.get("market_data", {})

    if not market_data:
        return {"risk_metrics": {}}

    try:
        # ---------- 1. Build per‑asset daily returns matrix ----------
        all_returns: dict[str, pd.Series] = {}
        for ticker, prices in market_data.items():
            if len(prices) > 1:
                closes = pd.Series([p["close"] for p in prices])
                all_returns[ticker] = closes.pct_change().dropna()

        if not all_returns:
            return {"risk_metrics": {"cvar_95": 0.0, "cvar_99": 0.0,
                                     "max_drawdown": 0.0, "sharpe_ratio": 0.0,
                                     "sortino_ratio": 0.0}}

        # ---------- 2. Portfolio-level equal-weight returns ----------
        min_len = min(len(s) for s in all_returns.values())
        aligned = pd.DataFrame({t: s.values[-min_len:] for t, s in all_returns.items()})
        portfolio_returns = aligned.mean(axis=1)   # equal-weight blend
        ret_array = portfolio_returns.to_numpy()

        # ---------- 3. Core Risk Metrics ----------
        # CVaR (Expected Shortfall)
        cvar_95 = float(np.mean(ret_array[ret_array <= np.percentile(ret_array, 5)]))
        cvar_99 = float(np.mean(ret_array[ret_array <= np.percentile(ret_array, 1)]))

        # Max Drawdown
        cumulative = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = float(drawdown.min())

        # Sharpe Ratio (annualized)
        excess_returns = ret_array - RISK_FREE_RATE
        sharpe = (excess_returns.mean() / ret_array.std(ddof=1)) * np.sqrt(252)

        # Sortino Ratio (annualized, downside deviation only)
        downside = ret_array[ret_array < 0]
        sortino = (excess_returns.mean() / downside.std(ddof=1)) * np.sqrt(252) if len(downside) > 1 else 0.0

        # ---------- 4. Asset-Level Risk Scoring ----------
        asset_risk: dict[str, dict] = {}
        for ticker, s in all_returns.items():
            vol = float(s.std() * np.sqrt(252))
            # Individual CVaR 95 for the asset
            a_rets = s.to_numpy()
            a_cvar_95 = float(np.mean(a_rets[a_rets <= np.percentile(a_rets, 5)]))
            
            # Status: "At Risk" if vol > 35% or CVaR95 < -4%
            status = "On Track"
            if vol > 0.35 or a_cvar_95 < -0.04:
                status = "At Risk"
            elif vol > 0.25:
                status = "Watchlist"
                
            asset_risk[ticker] = {
                "volatility": round(vol, 4),
                "cvar_95": round(a_cvar_95, 4),
                "status": status
            }

        # ---------- 5. Yule's Q — Tail Dependence Between Assets ----------
        yules_q: dict[str, float] = {}
        asset_list = list(all_returns.keys())
        for i in range(len(asset_list)):
            for j in range(i + 1, len(asset_list)):
                t1, t2 = asset_list[i], asset_list[j]
                r1 = all_returns[t1].values[-min_len:]
                r2 = all_returns[t2].values[-min_len:]
                neg1, neg2 = r1 < 0, r2 < 0
                a = int(np.sum(neg1 & neg2))
                b = int(np.sum(neg1 & ~neg2))
                c = int(np.sum(~neg1 & neg2))
                d = int(np.sum(~neg1 & ~neg2))
                denom = (a * d) + (b * c)
                yules_q[f"{t1}-{t2}"] = round(float(((a * d) - (b * c)) / denom), 3) if denom else 0.0

        # ---------- 6. Monte Carlo Simulation (10,000 paths, 1-year) ----------
        mu    = ret_array.mean()
        sigma = ret_array.std(ddof=1)
        # Set deterministic seed to ensure cache hits (stops API quota exhaustion)
        np.random.seed(42)
        # Simulate PROJECTION_DAYS daily returns across MONTE_CARLO_PATHS paths
        sim_daily = np.random.normal(mu, sigma, (PROJECTION_DAYS, MONTE_CARLO_PATHS))
        # Assume $100k portfolio
        initial_value = 100_000.0
        sim_paths = initial_value * np.cumprod(1 + sim_daily, axis=0)

        terminal_values = sim_paths[-1, :]       # Final values after 1 year
        prob_of_gain   = float(np.mean(terminal_values > initial_value))
        median_outcome = float(np.median(terminal_values))
        worst_5pct     = float(np.percentile(terminal_values, 5))
        best_5pct      = float(np.percentile(terminal_values, 95))

        metrics = {
            "cvar_95":                round(cvar_95, 6),
            "cvar_99":                round(cvar_99, 6),
            "max_drawdown":           round(max_drawdown, 6),
            "sharpe_ratio":           round(float(sharpe), 4),
            "sortino_ratio":          round(float(sortino), 4),
            "asset_risk":             asset_risk,
            "tail_dependence_yules_q": yules_q,
            "monte_carlo": {
                "simulation_paths":   MONTE_CARLO_PATHS,
                "projection_days":    PROJECTION_DAYS,
                "initial_value":      initial_value,
                "prob_of_gain_1yr":  round(prob_of_gain, 4),
                "median_outcome":     round(median_outcome, 2),
                "worst_5pct":         round(worst_5pct, 2),
                "best_5pct":          round(best_5pct, 2),
            }
        }

        logger.info("Risk analysis complete. Sharpe: %.2f, CVaR95: %.4f, Monte Carlo paths: %d",
                    sharpe, cvar_95, MONTE_CARLO_PATHS)
        return {"risk_metrics": metrics}

    except Exception as e:
        logger.error("Risk Analysis Error: %s", str(e), exc_info=True)
        return {"risk_metrics": {}}