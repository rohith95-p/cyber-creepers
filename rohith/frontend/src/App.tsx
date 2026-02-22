import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import type { FinalState } from './types'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [clientId, setClientId] = useState('PUNEETH_001')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [finalState, setFinalState] = useState<FinalState | null>(null)

  const generateReport = async () => {
    setLoading(true)
    setError(null)
    setFinalState(null)
    try {
      const res = await fetch(`${API_BASE}/api/generate-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: clientId }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(err.detail || 'Request failed')
      }
      const data = await res.json()
      setFinalState(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const report = finalState?.final_report ?? ''
  const metrics = finalState?.risk_metrics ?? {}
  const portfolio = finalState?.portfolio_assets ?? []
  const market = finalState?.market_data ?? {}
  const compliance = finalState?.compliance_status ?? 'Unknown'
  const profile = finalState?.client_profile ?? {}
  const mc = metrics.monte_carlo ?? {}
  const cvar = metrics.cvar_95 ?? 0
  const mdd = metrics.max_drawdown ?? 0
  const sharpe = metrics.sharpe_ratio ?? 0

  const chartData = (() => {
    const first = Object.keys(market)[0]
    if (!first || !market[first]?.length) return []
    return market[first].map((d) => ({ date: d.date, close: d.close })).reverse()
  })()

  const compData = [
    { client_id: clientId, sharpe, cvar },
    { client_id: 'BENCHMARK_SPY', sharpe: 0.8, cvar: -0.15 },
  ]
  const topPerformer = compData.reduce((a, b) => (a.sharpe > b.sharpe ? a : b))
  const safest = compData.reduce((a, b) => (a.cvar > b.cvar ? a : b))
  const avgSharpe = compData.reduce((s, c) => s + c.sharpe, 0) / compData.length
  const avgCvar = compData.reduce((s, c) => s + c.cvar, 0) / compData.length

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>🏦 Ivy Wealth AI</h1>
        <p className="tagline">
          <strong>Enterprise Portfolio Orchestrator</strong>
          <br />
          Analyze risk, simulate market volatility, and generate institutional-grade AI wealth reports using LangGraph.
        </p>
        <hr />
        <label>
          Client ID
          <input
            type="text"
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            placeholder="PUNEETH_001"
          />
        </label>
        <button
          className="btn-primary"
          onClick={generateReport}
          disabled={loading}
        >
          {loading ? 'Executing AI Pipeline...' : 'Generate Wealth Report'}
        </button>
        <hr />
        <p className="caption">v3.0.0 | Engine: LangGraph + OpenRouter</p>
      </aside>

      <main className="main">
        <header className="header">
          <h2>🏛️ Wealth Advisory Terminal</h2>
          <p><strong>Session:</strong> Active | <strong>Target Client:</strong> <code>{clientId}</code></p>
        </header>

        {error && (
          <div className="alert alert-error">
            <strong>System Failure:</strong> {error}
          </div>
        )}

        {!finalState && !loading && (
          <div className="alert alert-info">
            Select a client and click <strong>Generate Wealth Report</strong> to initiate the LangGraph orchestration.
          </div>
        )}

        <div className="metrics-row">
          <div className="metric-card">
            <span className="metric-label">CVaR (95%)</span>
            <span className="metric-value">{finalState ? `${(cvar * 100).toFixed(2)}%` : '--'}</span>
            <span className="metric-help">Conditional Value at Risk</span>
          </div>
          <div className="metric-card">
            <span className="metric-label">Max Drawdown</span>
            <span className="metric-value">{finalState ? `${(mdd * 100).toFixed(2)}%` : '--'}</span>
            <span className="metric-help">Peak-to-trough decline</span>
          </div>
          <div className="metric-card">
            <span className="metric-label">Sharpe Ratio</span>
            <span className="metric-value">{finalState ? sharpe.toFixed(2) : '--'}</span>
            <span className="metric-help">Risk-adjusted return</span>
          </div>
        </div>

        {finalState && (
          <>
            <section className="section">
              <h3>Historical Portfolio Performance</h3>
              {chartData.length > 0 ? (
                <div className="chart">
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
                      <XAxis dataKey="date" stroke="#8b949e" />
                      <YAxis stroke="#8b949e" />
                      <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d' }} />
                      <Line type="monotone" dataKey="close" stroke="#58a6ff" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="muted">No market data available.</p>
              )}
            </section>

            <section className="section">
              <h3>Analysis Workspace</h3>
              <div className="tabs">
                <TabPanel
                  tabs={[
                    { id: 'report', label: '📄 Executive Report' },
                    { id: 'goals', label: '🎯 Goal Planning' },
                    { id: 'consensus', label: '🧠 Advisor Consensus' },
                    { id: 'logic', label: '⚙️ System Logic' },
                    { id: 'compare', label: '📊 Client Comparison' },
                  ]}
                  defaultTab="report"
                >
                  {(active) => (
                    <>
                      {active === 'report' && (
                        <div className="tab-content">
                          <div className="report-box">
                            <ReactMarkdown>{report || 'No report generated.'}</ReactMarkdown>
                          </div>
                          <p><strong>Compliance Registry:</strong> <code>{compliance}</code></p>
                        </div>
                      )}
                      {active === 'goals' && (
                        <div className="tab-content">
                          <h4>🎯 Goal-Based Planning & Monte Carlo Analysis</h4>
                          <p className="muted">Powered by 10,000-path Monte Carlo simulation over a 1-year horizon.</p>
                          {Object.keys(mc).length > 0 && (
                            <div className="metrics-row">
                              <div className="metric-card">
                                <span className="metric-label">Probability of Gain (1yr)</span>
                                <span className="metric-value">{((mc.prob_of_gain_1yr ?? 0) * 100).toFixed(1)}%</span>
                              </div>
                              <div className="metric-card">
                                <span className="metric-label">Median Outcome (1yr)</span>
                                <span className="metric-value">${(mc.median_outcome ?? 0).toLocaleString()}</span>
                              </div>
                              <div className="metric-card">
                                <span className="metric-label">Worst 5%</span>
                                <span className="metric-value">${(mc.worst_5pct ?? 0).toLocaleString()}</span>
                              </div>
                              <div className="metric-card">
                                <span className="metric-label">Best 5%</span>
                                <span className="metric-value">${(mc.best_5pct ?? 0).toLocaleString()}</span>
                              </div>
                            </div>
                          )}
                          <div className="report-box">
                            <ReactMarkdown>{finalState?.goal_planning_analysis || 'No goal analysis available.'}</ReactMarkdown>
                          </div>
                        </div>
                      )}
                      {active === 'consensus' && (
                        <div className="tab-content">
                          <h4>👴 Warren Buffett</h4>
                          <div className="advisor-box advisor-info">{finalState?.buffett_analysis || 'No analysis found.'}</div>
                          <h4>📉 Benjamin Graham</h4>
                          <div className="advisor-box advisor-warning">{finalState?.graham_analysis || 'No analysis found.'}</div>
                          <h4>🚀 Modern Tech/Growth</h4>
                          <div className="advisor-box advisor-success">{finalState?.cathie_wood_analysis || 'No analysis found.'}</div>
                        </div>
                      )}
                      {active === 'logic' && (
                        <div className="tab-content">
                          <h4>👤 Client Persona</h4>
                          {Object.keys(profile).length > 0 ? (
                            <ul className="profile-list">
                              {Object.entries(profile).map(([k, v]) => (
                                <li key={k}><strong>{k.replace(/_/g, ' ')}:</strong> {String(v)}</li>
                              ))}
                            </ul>
                          ) : (
                            <p className="muted">No client profile data.</p>
                          )}
                          <h4>💼 Portfolio Structure</h4>
                          {portfolio.length > 0 ? (
                            <table className="data-table">
                              <thead>
                                <tr><th>Ticker</th><th>Quantity</th><th>Type</th></tr>
                              </thead>
                              <tbody>
                                {portfolio.map((p, i) => (
                                  <tr key={i}><td>{p.ticker}</td><td>{p.quantity}</td><td>{p.asset_type}</td></tr>
                                ))}
                              </tbody>
                            </table>
                          ) : (
                            <p className="muted">No portfolio data.</p>
                          )}
                          <h4>📈 Market Data Feed</h4>
                          {Object.keys(market).length > 0 ? (
                            <ul>
                              {Object.entries(market).map(([ticker, data]) => (
                                <li key={ticker}>{ticker}: {data?.length ?? 0} days</li>
                              ))}
                            </ul>
                          ) : (
                            <p className="muted">No market data.</p>
                          )}
                        </div>
                      )}
                      {active === 'compare' && (
                        <div className="tab-content">
                          <h4>🌍 Peer Group Analysis</h4>
                          <p>🏆 <strong>Top Performer:</strong> <code>{topPerformer.client_id}</code></p>
                          <p>🛡️ <strong>Safest Portfolio:</strong> <code>{safest.client_id}</code></p>
                          <p>Avg Sharpe: {avgSharpe.toFixed(2)} | Avg CVaR: {(avgCvar * 100).toFixed(2)}%</p>
                        </div>
                      )}
                    </>
                  )}
                </TabPanel>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

function TabPanel({
  tabs,
  defaultTab,
  children,
}: {
  tabs: { id: string; label: string }[]
  defaultTab: string
  children: (active: string) => React.ReactNode
}) {
  const [active, setActive] = useState(defaultTab)
  return (
    <>
      <div className="tab-buttons">
        {tabs.map((t) => (
          <button
            key={t.id}
            className={active === t.id ? 'tab-btn active' : 'tab-btn'}
            onClick={() => setActive(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>
      {children(active)}
    </>
  )
}
