---
name: trading-agents
description: TradingAgents risk & portfolio analysis — NO autonomous trade execution permitted
---

# TradingAgents Risk Analysis Skill

## Purpose
This skill provides **portfolio risk analysis** using the TradingAgents framework, including Conditional Value-at-Risk (CVaR) calculation, portfolio simulation, and risk-adjusted performance metrics.

## Reference Codebase
The full TradingAgents source is located at `references/` and contains the agent implementations, risk models, and backtesting utilities.

## Capabilities
| Capability | Description |
|------------|-------------|
| **CVaR Calculation** | Compute Conditional Value-at-Risk at configurable confidence levels (95%, 99%) |
| **Portfolio Simulation** | Monte Carlo simulation of portfolio returns over configurable horizons |
| **Drawdown Analysis** | Maximum drawdown and recovery period estimation |
| **Sharpe / Sortino Ratios** | Risk-adjusted return metrics |

## Usage
This skill receives market data (historical pricing from OpenBB) and portfolio composition, then outputs structured risk metrics:

```python
risk_output = {
    "cvar_95": -0.0342,           # 95% CVaR
    "cvar_99": -0.0518,           # 99% CVaR
    "max_drawdown": -0.1247,      # Maximum drawdown
    "sharpe_ratio": 1.23,         # Annualized Sharpe
    "sortino_ratio": 1.67,        # Annualized Sortino
    "simulation_paths": 10000,    # Monte Carlo paths run
}
```

---

> ⚠️ **FINRA/SEC COMPLIANCE MANDATE**
>
> **ALL outputs from this skill are ADVISORY ONLY.** The AI has **NO authority** to:
> - Execute any trades or orders
> - Rebalance portfolios autonomously
> - Submit any transaction to a broker or exchange
>
> Risk analysis results must be written to the CRM with `Status: "Pending Review"`.
> A licensed human advisor must review and explicitly approve any action before
> execution. Violation of this mandate is a regulatory breach.

---

## Integration Notes
- This skill is the **risk analysis node** in the LangGraph pipeline.
- It receives `market_data` from the `openbb-mcp` skill and outputs `risk_metrics` to the `finrobot-core` skill for report generation.
