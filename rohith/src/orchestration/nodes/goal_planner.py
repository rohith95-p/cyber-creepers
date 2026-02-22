"""
goal_planner.py — Phase 3: Goal-Based Planning Agent

Reads the client's financial goals from `client_profile` and the Monte Carlo
simulation output from `risk_metrics`, then calculates:
  - Probability of hitting the goal (wealth target by target date)
  - Whether the current portfolio is on-track or under-shooting
  - Specific, actionable rebalancing recommendations

Output key: `goal_planning_analysis` (str)
"""

import logging
import os
from typing import Any, Dict

from src.utils.error_handler import safe_llm_invoke
from src.utils.smart_cache import get_cached_or_compute
from src.utils.llm_provider import get_llm

logger = logging.getLogger(__name__)


def node_goal_planner(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares Monte Carlo simulation outputs against the client's explicit goals.
    Returns a structured goal-progress analysis and rebalancing recommendations.
    """
    logger.info("Running goal-based planning analysis...")

    client_profile: dict = state.get("client_profile", {})
    risk_metrics: dict  = state.get("risk_metrics", {})
    mc: dict            = risk_metrics.get("monte_carlo", {})
    portfolio_assets    = state.get("portfolio_assets", [])

    # ------------------------------------------------------------------
    # 1. Extract goal parameters from client profile
    # ------------------------------------------------------------------
    goal_amount       = client_profile.get("goal_amount_usd", 1_000_000)
    time_horizon_yrs  = client_profile.get("time_horizon_years", 20)
    current_portfolio_value = client_profile.get("current_portfolio_value_usd", 100_000)
    risk_tolerance    = client_profile.get("risk_tolerance", "moderate")
    goal_description  = client_profile.get("primary_goal", "Wealth accumulation for retirement")

    # ------------------------------------------------------------------
    # 2. Probability of success from Monte Carlo (scale to full horizon)
    # ------------------------------------------------------------------
    prob_gain_1yr  = mc.get("prob_of_gain_1yr", 0.55)
    median_outcome = mc.get("median_outcome", current_portfolio_value * 1.07)
    worst_5pct     = mc.get("worst_5pct", current_portfolio_value * 0.85)
    best_5pct      = mc.get("best_5pct", current_portfolio_value * 1.30)

    # Approx compound: assume median annual growth rate implied by 1-yr median
    if current_portfolio_value > 0:
        annual_growth_rate = (median_outcome / current_portfolio_value) - 1
    else:
        annual_growth_rate = 0.07  # fallback 7%

    # Project median outcome over full time horizon
    projected_value = current_portfolio_value * ((1 + annual_growth_rate) ** time_horizon_yrs)

    # On-track flag
    on_track = projected_value >= goal_amount
    gap = goal_amount - projected_value
    required_growth_rate = (goal_amount / current_portfolio_value) ** (1 / max(time_horizon_yrs, 1)) - 1

    summary_data = {
        "goal_amount": f"${goal_amount:,.0f}",
        "time_horizon_years": time_horizon_yrs,
        "current_value": f"${current_portfolio_value:,.0f}",
        "projected_value_median": f"${projected_value:,.0f}",
        "prob_of_gain_1yr": f"{prob_gain_1yr * 100:.1f}%",
        "on_track": on_track,
        "gap": f"${abs(gap):,.0f} {'surplus' if on_track else 'shortfall'}",
        "required_annual_growth": f"{required_growth_rate * 100:.2f}%",
        "implied_annual_growth": f"{annual_growth_rate * 100:.2f}%",
        "worst_5pct_1yr": f"${worst_5pct:,.0f}",
        "best_5pct_1yr": f"${best_5pct:,.0f}",
    }

    # ------------------------------------------------------------------
    # 3. LLM: Generate natural-language goal analysis + recommendations
    # ------------------------------------------------------------------
    tickers = ", ".join(a.get("ticker", "") for a in portfolio_assets if a.get("ticker"))
    status_label = "ON TRACK ✅" if on_track else "AT RISK ⚠️"

    prompt = f"""
You are a senior Certified Financial Planner (CFP). Your client has the following goal:
- Primary Goal: {goal_description}
- Target Wealth: ${goal_amount:,.0f}
- Time Horizon: {time_horizon_yrs} years
- Current Portfolio Value: ${current_portfolio_value:,.0f}
- Risk Tolerance: {risk_tolerance}

Based on a 10,000-path Monte Carlo simulation of their current portfolio ({tickers}),
here are the projected outcomes:
- 1-Year Probability of Positive Return: {prob_gain_1yr * 100:.1f}%
- 1-Year Median Portfolio Value: ${median_outcome:,.0f}
- 1-Year Best-Case (95th percentile): ${best_5pct:,.0f}
- 1-Year Worst-Case (5th percentile): ${worst_5pct:,.0f}
- Implied Annual Growth Rate: {annual_growth_rate * 100:.2f}%
- Required Annual Growth Rate to Hit Goal: {required_growth_rate * 100:.2f}%
- {time_horizon_yrs}-Year Projected Value (median path): ${projected_value:,.0f}
- Goal Status: {status_label}
- Gap: {summary_data['gap']}

Write a concise Goal Progress Report (3-4 paragraphs max) that:
1. Opens with whether the client is on track or at risk, citing the key numbers
2. Explains what the simulation implies for their long-term goal
3. Provides 2-3 specific, concrete rebalancing or savings recommendations appropriate for their risk tolerance
4. Closes with a motivating but realistic outlook

Use plain but professional language. Do not use generic advice. Be specific.
"""

    analysis_text = ""
    try:
        def _call_goal_llm():
            llm = get_llm(temperature=0.3)
            resp = safe_llm_invoke(llm, prompt)
            return resp.content.strip()
            
        # Cache signature based on client and goal numbers, protect API quota
        payload = {"goals": summary_data, "tickers": tickers}
        client_id = state.get("client_id", "Unknown")
        
        analysis_text = get_cached_or_compute("goal_planner", client_id, payload, _call_goal_llm)
        
    except Exception as e:
        logger.error("Goal planner LLM error: %s", str(e))
        # Fallback: return a structured text summary without LLM
        analysis_text = f"""
**Goal Progress Report — {status_label}**

Your current portfolio is projected to grow to approximately **{summary_data['projected_value_median']}** 
over {time_horizon_yrs} years at an implied annual growth rate of {summary_data['implied_annual_growth']}.

{'This meets your target of ' + summary_data['goal_amount'] + '.' if on_track else 'This falls short of your target of ' + summary_data['goal_amount'] + ' by approximately ' + summary_data['gap'] + '.'}

**Monte Carlo Snapshot (1-Year):**
- Probability of positive return: {summary_data['prob_of_gain_1yr']}
- Median outcome: ${median_outcome:,.0f}
- Worst 5% scenario: {summary_data['worst_5pct_1yr']}
- Best 5% scenario: {summary_data['best_5pct_1yr']}

**Required annual growth to reach goal:** {summary_data['required_annual_growth']}

*Recommendation: Consult with your advisor to review asset allocation and savings rate.*
""".strip()

    # Return both structured data and narrative
    full_analysis = f"{analysis_text}\n\n---\n**Simulation Summary:** {summary_data}"
    return {"goal_planning_analysis": full_analysis}
