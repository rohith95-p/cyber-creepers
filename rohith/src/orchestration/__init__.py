"""
orchestration — Wealth Management multi-agent pipeline built on LangGraph.

Entry point
-----------
>>> from orchestration import build_graph
>>> app = build_graph()
>>> result = app.invoke({"client_id": "001ABC123"})
"""

from .supervisor_graph import build_graph, app

__all__ = ["build_graph", "app"]
