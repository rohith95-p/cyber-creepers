# 🏦 Ivy Wealth AI: Institutional Portfolio Orchestrator
**Comprehensive Project Deep Dive & Technical Reference**

This document provides a highly detailed, foundational breakdown of the entire **Ivy Wealth AI** project. It is designed to equip you with everything needed to thoroughly understand the architecture, logic, and libraries so you can explain the system confidently to your teammates or stakeholders.

---

## 1. Project Overview & Objective
**Ivy Wealth AI** is an institutional-grade, AI-driven wealth management platform. The goal is to provide Relationship Managers (RMs) and Financial Advisors with real-time, automated, deeply analytical portfolio reviews. 

Instead of relying on a single AI prompt, the platform orchestrates a **"Brain Trust" of multi-agent AI personas**, simulating a boardroom of expert analysts (e.g., Warren Buffett for value, Benjamin Graham for risk, Cathie Wood for growth). These agents analyze client data and market trends simultaneously, culminating in a highly structured, consensus-driven final wealth report.

---

## 2. High-Level System Architecture
The application follows a modern decoupled architecture:
1. **Frontend**: A highly polished, responsive Single Page Application (SPA) built with React and Vite. It serves as the "Wealth Overview" terminal.
2. **Backend Engine**: A robust API built with FastAPI serving Python-based AI orchestration workflows via LangGraph.
3. **External Integrations**: Salesforce for Client Data (CRM), Yahoo Finance for Live Market Data, and OpenRouter for Large Language Model (LLM) access.

---

## 3. The Backend: Python, FastAPI, and LangGraph
The backend (`/rohith` directory) is the brain of the operation. It is built to be asynchronous, modular, and highly scalable.

### 3.1 Key Libraries Used
*   **FastAPI**: The core web framework. Chosen for its extreme speed (built on Starlette) and native async support. It exposes the endpoints (e.g., `/api/clients`, `/api/generate-report`) that the frontend consumes.
*   **Uvicorn**: The ASGI web server implementation used to run the FastAPI application.
*   **LangGraph**: The most critical library in the project. It is an extension of LangChain used to build stateful, multi-actor applications. It allows us to define the flow of AI analysis as a directed graph rather than a linear chain.
*   **LangChain**: Provides the base abstractions for interacting with LLMs (creating prompts, managing tools, parsing outputs).
*   **yfinance**: Used specifically in the `fetch_market` node to pull real-time macro-economic data and ticker performance.
*   **simple_salesforce**: The integration layer allowing the backend to pull exact client portfolios securely from the Salesforce CRM.
*   **python-dotenv**: Manages environment variables (API keys, Salesforce credentials) securely.

### 3.2 The LangGraph Pipeline (How a Report is Made)
When the user clicks "Generate Wealth Report", a LangGraph "StateGraph" is triggered in `supervisor_graph.py`. Here is the exact node-by-node teardown:

1.  **Node 1: `profile_client`**
    *   **Action**: Receives the basic Salesforce client schema.
    *   **Logic**: Uses an LLM to generate a deep psychological and financial profile of the client (Risk tolerance, liquidity needs, investment horizon).
2.  **Node 2: `fetch_market`**
    *   **Action**: Independent of the client, this node fetches real-world macro data using `yfinance`. It looks at S&P 500 trends, volatility indices, and specific ticker performance relevant to the client.
3.  **Node 3: `analyze_risk`**
    *   **Action**: Takes the client's current portfolio and mathematically evaluates exposure, diversification, and Sharpe ratios.
4.  **Node 4: `persona_ensemble` (The Brain Trust)**
    *   **Action**: This is the "magic" step. It runs **in parallel**. The system spins up three distinct LLM prompts:
        *   *The Value Investor (Buffett style)*: Looks for intrinsic value and dividend safety.
        *   *The Risk Manager (Graham style)*: Looks for margin of safety and downside protection.
        *   *The Growth Strategist (Wood style)*: Looks for disruptive innovation and alpha opportunities.
    *   **Logic**: All three agents analyze the outputs of Nodes 1, 2, and 3 simultaneously.
5.  **Node 5: `compile_master_report` (The Supervisor)**
    *   **Action**: Collects the three persona reports.
    *   **Logic**: It acts as the Chief Investment Officer. It resolves conflicts between the personas and forces the output into a strict markdown format (Investment Outlook, Key Strengths/Analysis, Overall Strategic Recommendation).

---

## 4. The Frontend: React, Vite, and TailwindCSS
The frontend (`/frontend` directory) is where the financial advisors interact with the AI. It has been polished to feature an "Ultra-Premium Institutional" aesthetic.

### 4.1 Key Libraries Used
*   **React (via Vite)**: The UI framework. Vite is used instead of Create React App for significantly faster hot-module replacement and optimized builds.
*   **TailwindCSS**: The utility-first CSS framework used for styling. It allows for rapid prototyping of the dark-mode, glassmorphism UI.
*   **Recharts**: The library rendering the interactive pie charts (Risk Composition) and statistics on the dashboard.
*   **ReactMarkdown & @tailwindcss/typography**: Crucial for rendering the AI's output. Because LLMs return Markdown text (e.g., `**bold**`, `### Header`), these libraries parse that raw text into beautifully styled HTML elements.
*   **Axios**: Manages HTTP requests to the FastAPI backend.

### 4.2 Architecture of `App.jsx`
The main file `App.jsx` manages the complete state of the application:
*   **State Management**: It uses `useState` to track the active client, the current API response (the report), and the active navigation tab (Wealth Overview vs. Wealth Report).
*   **The 3-Box UI Splitting Logic**: Because the backend supervisor generates a single long markdown string, `App.jsx` uses Regex (`/\*\*Key Strengths:\*\*/i` and `/\*\*Overall:\*\*/i`) to physically split the string into three pieces. These pieces are mapped to three custom `<ReportBox>` components.
*   **Error Boundaries**: A `MarkdownErrorBoundary` class is implemented to ensure that if the AI generates malformed markdown, the app gracefully catches it rather than crashing to a blank screen.
*   **Glassmorphism Engine**: Custom CSS in `index.css` (`.glass-card`) applies heavy backdrop blurs, subtle linear gradients, and animated hover states to replicate high-end financial terminals like a Bloomberg workstation.

---

## 5. Security & Infrastructure Details
*   **API Key Rotation**: The system connects via OpenRouter (`OPENROUTER_API_KEY` in `.env`). The backend `llm_provider.py` is configured to handle fallback logic if an API key is exhausted due to rate limits.
*   **Salesforce Auth**: Authentication is handled via `SF_USERNAME`, `SF_PASSWORD`, and `SF_SECURITY_TOKEN`. The system supports direct access token bypass if SOAP logins are restricted.
*   **CORS Configuration**: The FastAPI backend explicitly allows Cross-Origin requests from the Vite frontend running on `localhost:5173` to prevent browser security blocks during development.

---

## 6. How to Run the Project (For Teammates)
To run the project fresh, two terminals are required:

**Terminal 1 (Backend - The AI Engine):**
1. `cd rohith`
2. Ensure you are in the python virtual environment.
3. `uvicorn api:app --host 0.0.0.0 --port 8000 --reload`
*(This starts the LangGraph engine on port 8000)*

**Terminal 2 (Frontend - The UI Terminal):**
1. `cd frontend`
2. `npm install` (if first time)
3. `npm run dev`
*(This starts the React dashboard on port 5173)*

---

### Conclusion
By combining **LangGraph's multi-agent routing** with a **Glassmorphism React UI**, Ivy Wealth AI transcends basic API wrappers. It represents a true "Agentic Workflow"—where AI actors collaborate, debate, and compile insights automatically, presented in an enterprise-ready dashboard. This wraps up the complete development cycle of the Fiduciary Sentinel project.
