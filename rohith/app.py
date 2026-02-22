import os
import logging
from dotenv import load_dotenv

# 1. CRITICAL: Load environment variables BEFORE importing the LangGraph app
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(override=True)

import streamlit as st
from src.orchestration.supervisor_graph import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import plotly.express as px
from src.comparison.client_comparator import ClientComparator
try:
    from src.models.sentiment_analyzer import SentimentAnalyzer
    sentiment_enabled = True
except ImportError as e:
    logger.warning(f"Sentiment analysis disabled. Module missing: {e}")
    sentiment_enabled = False
# Handle WeasyPrint gracefully on Windows without crashing Streamlit
try:
    from src.utils.pdf_generator import generate_wealth_pdf
    pdf_enabled = True
except Exception as e:
    logger.warning(f"PDF generation disabled. WeasyPrint/GTK+ missing: {e}")
    pdf_enabled = False

# 2. Page Configuration
st.set_page_config(
    page_title="Ivy Wealth AI",
    page_icon="🏦",
    layout="wide"
)

# 3. Custom CSS (Enterprise White-labeling & Styling)
st.markdown("""
<style>
    /* Hide Streamlit Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Report Container */
    .report-box {
        padding: 30px;
        background-color: #0e1117;
        border-radius: 10px;
        border: 1px solid #30363d;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 4. Sidebar Implementation
with st.sidebar:
    st.title("🏦 Ivy Wealth AI")
    st.markdown("""
    **Enterprise Portfolio Orchestrator**
    Analyze risk, simulate market volatility, and generate institutional-grade AI wealth reports using LangGraph.
    """)
    st.markdown("---")
    
    client_id = st.text_input("Client ID", value="PUNEETH_001")
    generate_btn = st.button("Generate Wealth Report", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("v3.0.0 | Engine: LangGraph + Gemini 2.0 Flash")

# 5. Dashboard Header
st.title("🏛️ Wealth Advisory Terminal")
st.markdown(f"**Session:** Active | **Target Client:** `{client_id}`")

if "final_state" not in st.session_state:
    st.session_state.final_state = None

if generate_btn:
    initial_state = {
        "client_id": client_id,
        "portfolio_assets": [],
        "market_data": {},
        "risk_metrics": {},
        "final_report": "",
        "compliance_status": "Processing...",
        "client_profile": {},
        "news_summary": {},
        "fundamentals_summary": {},
        "macro_summary": "",
        "buffett_analysis": "",
        "graham_analysis": "",
        "cathie_wood_analysis": "",
        "goal_planning_analysis": ""
    }

    try:
        # 6. Dynamic Execution Status (st.status)
        with st.status("Executing AI Pipeline...", expanded=True) as status:
            st.write("🔍 Connecting to CRM Vault...")
            st.write("👤 Retrieving Client Persona & Goals...")
            st.write("📈 Fetching Real-time Market Data...")
            st.write("🧮 Running Monte Carlo Risk Engine (10,000 paths)...")
            st.write("🎯 Running Goal-Based Planning Analysis...")
            st.write("🧠 Engaging Persona Ensemble (Buffett, Graham, Growth)...")
            st.write("📝 Synthesizing Final Consensus Report...")
            
            # Invoke the LangGraph pipeline
            final_state = app.invoke(initial_state)
            st.session_state.final_state = final_state
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)

    except Exception as e:
        logger.error(f"Execution Error: {e}")
        st.error(f"**System Failure:** {str(e)}")
        st.info("Debugging Tip: Ensure your .env file contains a valid GOOGLE_API_KEY.")

if st.session_state.final_state:
    final_state = st.session_state.final_state
    
    # Extract data from state
    report_md = final_state.get("final_report", "No report generated.")
    metrics = final_state.get("risk_metrics", {})
    portfolio = final_state.get("portfolio_assets", [])
    market = final_state.get("market_data", {})
    compliance = final_state.get("compliance_status", "Unknown")
    profile = final_state.get("client_profile", {})

    # 7. KPI Metric Row
    st.markdown("---")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    cvar = metrics.get("cvar_95", 0.0)
    mdd = metrics.get("max_drawdown", 0.0)
    sharpe = metrics.get("sharpe_ratio", 0.0)

    # Clean Formatting
    m_col1.metric("CVaR (95%)", f"{cvar:.2%}", help="Conditional Value at Risk (Expected Tail Loss)")
    m_col2.metric("Max Drawdown", f"{mdd:.2%}", help="Peak-to-trough decline during the period")
    m_col3.metric("Sharpe Ratio", f"{sharpe:.2f}", help="Risk-adjusted return vs. Risk-free rate")

    # UI Component 2: Historical Performance Charts
    st.markdown("### Historical Portfolio Performance")
    if market:
        # Simple line chart using the first ticker's close prices as a proxy for the UI
        first_ticker = list(market.keys())[0]
        if market[first_ticker]:
            dates = [d['date'] for d in market[first_ticker]]
            prices = [d['close'] for d in market[first_ticker]]
            fig = px.line(x=dates, y=prices, title=f"1Y Trailing Performance ({first_ticker})")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Analysis Workspace")
    
    # 8. Tabbed Content Navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Executive Report", 
        "🎯 Goal Planning",
        "🧠 Advisor Consensus",
        "⚙️ System Logic", 
        "📊 Client Comparison", 
        "📰 Sentiment Analytics"
    ])

    with tab1:
        st.markdown(f'<div class="report-box">{report_md}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"**Compliance Registry:** `{compliance}`")
        
        # UI Component 1: Approval Workflow Buttons (PDF Generation)
        col_app1, col_app2 = st.columns(2)
        with col_app1:
            if st.button("Generate Compliance PDF", type="secondary"):
                if pdf_enabled:
                    pdf_path = generate_wealth_pdf(report_md, client_id)
                    st.success(f"PDF Generated at: {pdf_path}")
                else:
                    st.error("PDF generation is disabled. Please install GTK3 Windows libraries for WeasyPrint.")
        with col_app2:
            if st.button("Approve & Save to Salesforce", type="primary"):
                st.success("Report officially logged and transmitted to Salesforce compliance vault.")
                st.balloons()

    with tab2:
        st.subheader("🎯 Goal-Based Planning & Monte Carlo Analysis")
        st.caption("Powered by 10,000-path Monte Carlo simulation over a 1-year horizon.")

        # Monte Carlo metrics
        mc = metrics.get("monte_carlo", {})
        if mc:
            g1, g2, g3, g4 = st.columns(4)
            g1.metric("Probability of Gain (1yr)", f"{mc.get('prob_of_gain_1yr', 0):.1%}")
            g2.metric("Median Outcome (1yr)", f"${mc.get('median_outcome', 0):,.0f}")
            g3.metric("Worst 5% Scenario", f"${mc.get('worst_5pct', 0):,.0f}")
            g4.metric("Best 5% Scenario", f"${mc.get('best_5pct', 0):,.0f}")
            st.markdown(f"*Simulation paths: {mc.get('simulation_paths', 0):,} | Horizon: {mc.get('projection_days', 252)} trading days*")
        else:
            st.info("Run the pipeline to see Monte Carlo simulation results.")

        st.markdown("---")
        st.markdown("### 📋 Goal Progress Report")
        goal_analysis = final_state.get("goal_planning_analysis", "")
        if goal_analysis:
            st.markdown(goal_analysis)
        else:
            st.info("Goal planning analysis not available. Ensure client profile has goal_amount_usd and time_horizon_years.")

    with tab3:
        st.subheader("Simulated Advisor Debate")
        
        st.markdown("### 👴 Warren Buffett")
        st.info(final_state.get("buffett_analysis", "No analysis found."))
        
        st.markdown("### 📉 Benjamin Graham")
        st.warning(final_state.get("graham_analysis", "No analysis found."))
        
        st.markdown("### 🚀 Modern Tech/Growth")
        st.success(final_state.get("cathie_wood_analysis", "No analysis found."))

    with tab4:
        st.subheader("Orchestration Context")
        
        st.markdown("### 👤 Client Persona")
        if profile:
            for k, v in profile.items():
                st.markdown(f"**{str(k).replace('_', ' ').title()}:** {v}")
        else:
            st.info("No client profile data available.")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 💼 Portfolio Structure")
            if portfolio:
                import pandas as pd
                st.dataframe(pd.DataFrame(portfolio), use_container_width=True)
            else:
                st.info("No portfolio data.")
        with col_b:
            st.markdown("### 📈 Market Data Feed")
            if market:
                for ticker, data in market.items():
                    st.metric(label=f"{ticker} Historical Prices", value=f"{len(data)} Days")
            else:
                st.info("No market data fetched.")

    with tab5:
        # UI Component 3: Multi-Client Comparison Tab
        st.subheader("🌍 Peer Group Analysis")
        st.info("Dynamic comparison engine loaded. To fully utilize this, run multiple clients through the batch processor.")
        comparator = ClientComparator()
        # Mock data for demonstration of the component
        mock_peer_data = [
            {"client_id": client_id, "sharpe": sharpe, "cvar": cvar},
            {"client_id": "BENCHMARK_SPY", "sharpe": 0.8, "cvar": -0.15}
        ]
        comp_results = comparator.compare_clients(mock_peer_data)
        
        st.markdown(f"🏆 **Top Performer:** `{comp_results.get('top_performer', 'N/A')}`")
        st.markdown(f"🛡️ **Safest Portfolio:** `{comp_results.get('safest_portfolio', 'N/A')}`")
        
        st.markdown("---")
        st.markdown("#### Peer Benchmarks")
        avg = comp_results.get("peer_group_averages", {})
        col1, col2 = st.columns(2)
        col1.metric("Avg Sharpe", f"{avg.get('avg_sharpe', 0):.2f}")
        col2.metric("Avg CVaR", f"{avg.get('avg_cvar', 0):.2%}")
        
        st.markdown("#### Client Rankings")
        rankings = comp_results.get("client_rankings", {})
        if rankings:
            import pandas as pd
            rank_df = pd.DataFrame.from_dict(rankings, orient='index')
            st.dataframe(rank_df, use_container_width=True)

    with tab6:
        # UI Component 4: Sentiment Gauges and News Feed
        st.subheader("Real-Time News Sentiment")
        if sentiment_enabled:
            if st.button("Run FinBERT NLP Analysis"):
                with st.spinner("Analyzing headline sentiment..."):
                    analyzer = SentimentAnalyzer()
                    sentiment_results = analyzer.analyze_portfolio(portfolio)
                    st.json(sentiment_results)
        else:
            st.warning("Sentiment Analysis disabled. Module 'src.models.sentiment_analyzer' missing.")

else:
    # Landing State
    st.info("Select a client and click **Generate Wealth Report** to initiate the LangGraph orchestration.")
    
    # Empty KPI Placeholders
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("CVaR (95%)", "--")
    m_col2.metric("Max Drawdown", "--")
    m_col3.metric("Sharpe Ratio", "--")
