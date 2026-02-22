from langgraph.graph import StateGraph, END
from .state import AgentState

# 2. Node Imports (Ensure these names exist in your node files!)
from .nodes.fetch_crm import fetch_crm
from .nodes.profile_client import node_profile_client
from .nodes.fetch_market import node_fetch_market_data
from .nodes.analyze_risk import node_analyze_risk
from .nodes.summarize_news import node_summarize_news
from .nodes.summarize_fundamentals import node_summarize_fundamentals
from .nodes.summarize_macro import node_summarize_macro
from .nodes.persona_ensemble import node_persona_ensemble
from .nodes.compile_master_report import compile_master_report
from .nodes.save_draft import node_save_draft
from .nodes.goal_planner import node_goal_planner

# 3. Graph Logic
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("fetch_portfolio", fetch_crm)
    workflow.add_node("profile_client", node_profile_client)
    workflow.add_node("fetch_market", node_fetch_market_data)
    workflow.add_node("analyze_risk", node_analyze_risk)
    workflow.add_node("summarize_news", node_summarize_news)
    workflow.add_node("summarize_fundamentals", node_summarize_fundamentals)
    workflow.add_node("summarize_macro", node_summarize_macro)
    workflow.add_node("persona_ensemble", node_persona_ensemble)
    workflow.add_node("compile_master_report", compile_master_report)
    workflow.add_node("save_draft", node_save_draft)
    workflow.add_node("goal_planner", node_goal_planner)

    workflow.set_entry_point("fetch_portfolio")
    workflow.add_edge("fetch_portfolio", "profile_client")
    workflow.add_edge("profile_client", "fetch_market")
    
    # Run risk and summarizers after market data
    workflow.add_edge("fetch_market", "analyze_risk")
    workflow.add_edge("analyze_risk", "goal_planner")
    workflow.add_edge("goal_planner", "summarize_news")
    workflow.add_edge("summarize_news", "summarize_fundamentals")
    workflow.add_edge("summarize_fundamentals", "summarize_macro")
    
    # Run the unified ensemble persona analysis
    workflow.add_edge("summarize_macro", "persona_ensemble")
    
    # Send the ensemble directly to the synthesizer
    workflow.add_edge("persona_ensemble", "compile_master_report")
    
    workflow.add_edge("compile_master_report", "save_draft")
    workflow.add_edge("save_draft", END)

    return workflow.compile()

app = build_graph()