---
name: openbb-mcp
description: OpenBB MCP data server — provides equity and news data to downstream agents via Model Context Protocol
---

# OpenBB MCP Skill

## Purpose
This skill wraps the **OpenBB Platform** as an MCP (Model Context Protocol) server, exposing equity pricing and financial news endpoints to all downstream agents in the wealth management pipeline.

## Reference Codebase
The full OpenBB source is located at `references/` and contains the platform SDK, data providers, and MCP server implementation.

## Server Configuration
- **Host**: `127.0.0.1`
- **Port**: `8080`
- **Allowed Categories**: `equity`, `news`
- **Endpoint**: `http://127.0.0.1:8080/mcp/`
- **Setup Script**: `start_openbb_mcp.ps1` (creates venv, installs deps, loads `.env`, launches server)

## Available Data Operations
| Operation | Description |
|-----------|-------------|
| `equity.price.historical` | Fetch historical OHLCV data for a given ticker and date range |
| `equity.fundamental.overview` | Company fundamentals and financial ratios |
| `equity.estimates.consensus` | Analyst consensus estimates |
| `news.search` | Search financial news by keyword or ticker |

## Usage
Downstream agents (e.g., `trading-agents` for risk analysis) call this server via the MCP protocol. The server is registered in the project-root `mcp.json`.

## API Keys
All provider-specific API keys (e.g., Polygon, Alpha Vantage, FMP) must be defined in the project-root `.env` file. The setup script loads them automatically before server launch.
