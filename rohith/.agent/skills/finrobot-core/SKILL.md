---
name: finrobot-core
description: FinRobot Director Agent — orchestrates sub-agents for financial analysis and report generation
---

# FinRobot Core Skill

## Purpose
This skill provides the **FinRobot Director Agent**, a multi-agent orchestration framework purpose-built for financial analysis and wealth management reporting.

## Reference Codebase
The full FinRobot source is located at `references/` and contains the agent implementations, prompt templates, and data-processing pipelines.

## How to Instantiate the Director Agent

1. **Import** the Director Agent from the reference codebase:
   ```python
   from references.finrobot.agents import DirectorAgent
   ```

2. **Configure** the agent with the required LLM backend and API keys loaded from the project-root `.env` file.

3. **Invoke** the agent by passing a structured `AgentState` dictionary containing:
   - `client_id` — the CRM client identifier
   - `portfolio_assets` — list of ticker symbols and quantities
   - `market_data` — historical price data (from OpenBB)
   - `risk_metrics` — CVaR and other risk outputs (from TradingAgents)

4. **Output**: The Director Agent produces a structured **Markdown wealth management report** summarizing portfolio performance, risk exposure, and recommendations.

## Sub-Agent Roles
| Agent | Responsibility |
|-------|---------------|
| **Market Analyst** | Interprets pricing trends and technical indicators |
| **Risk Analyst** | Evaluates portfolio risk using quantitative metrics |
| **Report Writer** | Composes the final client-facing Markdown report |

## Integration Notes
- The Director Agent is the **terminal node** in the LangGraph pipeline — it receives all upstream state and produces the final deliverable.
- Reports must be written back to the CRM via the `langchain-salesforce` skill with `Status: "Pending Review"`.
