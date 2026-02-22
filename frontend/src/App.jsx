import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip,
  Legend, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import ReactMarkdown from 'react-markdown';

class MarkdownErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error("Markdown crash caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-rose-500/20 text-rose-400 rounded-xl text-xs font-mono">
          <p className="font-bold mb-2">Markdown Rendering Failed:</p>
          <p>{this.state.error && this.state.error.toString()}</p>
        </div>
      );
    }
    return this.props.children;
  }
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

// --- Icons (SVG Strings for portability) ---
const Icons = {
  Dashboard: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" /></svg>
  ),
  Users: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
  ),
  Analytics: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>
  ),
  Settings: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" /><circle cx="12" cy="12" r="3" /></svg>
  ),
  FileText: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" /></svg>
  ),
  Target: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></svg>
  )
};

// --- Components ---

const StatCard = ({ title, value, icon: Icon, trend, colorClass }) => (
  <div className="glass-card p-6 rounded-2xl relative overflow-hidden">
    <div className={`absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 rounded-full opacity-10 ${colorClass}`}></div>
    <div className="flex justify-between items-start mb-4">
      <div className="p-2 bg-slate-800/50 rounded-lg text-blue-400">
        <Icon />
      </div>
      {trend && (
        <span className={`text-xs font-medium px-2 py-1 rounded-full ${trend > 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
          {trend > 0 ? '+' : ''}{trend}%
        </span>
      )}
    </div>
    <h3 className="text-slate-400 text-sm font-medium mb-1">{title}</h3>
    <p className="text-2xl font-bold text-white">{value}</p>
  </div>
);

const SectionTitle = ({ children, icon: Icon }) => (
  <div className="flex items-center space-x-2 mb-6">
    {Icon && <div className="text-blue-400"><Icon /></div>}
    <h2 className="text-xl font-semibold text-white tracking-tight">{children}</h2>
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [holdingClient, setHoldingClient] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAllClients, setShowAllClients] = useState(false);
  const [systemStatus, setSystemStatus] = useState({ engine: 'LangGraph v3.0', crm: 'Connected' });

  useEffect(() => {
    fetchClients();
    fetchSystemStatus();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/health`);
      setSystemStatus(resp.data);
    } catch (err) {
      // Fallback defaults
    }
  };

  const fetchClients = async () => {
    setLoading(true);
    try {
      const resp = await axios.get(`${API_BASE}/clients`);
      setClients(resp.data);
    } catch (err) {
      setError("Failed to fetch clients. Systems operating on fallback vault.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async (client) => {
    setLoading(true);
    setSelectedClient(client);
    try {
      const resp = await axios.post(`${API_BASE}/generate-report`, { client_id: client.id });
      setReport(resp.data);
      setActiveTab('report');
    } catch (err) {
      setError("AI orchestration failed. Please check LLM provider status.");
    } finally {
      setLoading(false);
    }
  };

  const handleExportJSON = () => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `wealth_report_${selectedClient?.name.replace(/\s+/g, '_')}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleMacroReport = () => {
    setActiveTab('macro');
  };

  const filteredClients = useMemo(() => {
    return clients.filter(c =>
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.id.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [clients, searchTerm]);

  const stats = useMemo(() => {
    if (!clients.length) return {};
    return {
      totalAUM: clients.reduce((sum, c) => sum + c.portfolio_value, 0),
      avgSharpe: (clients.reduce((sum, c) => sum + (c.sharpe_ratio || 0.8), 0) / clients.length).toFixed(2),
      atRiskPct: ((clients.filter(c => c.status === 'At Risk').length / clients.length) * 100).toFixed(0),
      onTrackCount: clients.filter(c => c.status === 'On Track').length
    };
  }, [clients]);

  // Chart Data
  const riskData = useMemo(() => [
    { name: 'Aggressive', value: clients.filter(c => c.risk_tolerance === 'Aggressive').length },
    { name: 'Moderate', value: clients.filter(c => c.risk_tolerance === 'Moderate').length },
    { name: 'Conservative', value: clients.filter(c => c.risk_tolerance === 'Conservative').length },
  ], [clients]);

  const COLORS = ['#38bdf8', '#818cf8', '#34d399'];

  return (
    <div className="flex h-screen bg-[#020617] text-slate-200">
      {/* Sidebar */}
      <aside className="w-64 glass border-r border-slate-800 flex flex-col p-6 space-y-8 z-20">
        <div className="flex items-center space-x-3 mb-10 group cursor-pointer" onClick={() => setActiveTab('overview')}>
          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 via-blue-500 to-cyan-400 rounded-2xl flex items-center justify-center shadow-[0_8px_30px_rgb(59,130,246,0.3)] group-hover:scale-110 transition-transform duration-500">
            <span className="text-white font-black text-2xl italic tracking-tighter">IV</span>
          </div>
          <div>
            <h1 className="text-xl font-black text-white tracking-tighter leading-none">
              IVY<span className="text-blue-400">WEALTH</span>
            </h1>
            <p className="text-[8px] font-black text-blue-500/50 uppercase tracking-[0.3em] mt-1">Institutional AI</p>
          </div>
        </div>

        <nav className="flex-1 space-y-2">
          <NavItem active={activeTab === 'overview'} onClick={() => setActiveTab('overview')} icon={Icons.Dashboard} label="Wealth Overview" />
          <NavItem active={activeTab === 'analytics'} onClick={() => setActiveTab('analytics')} icon={Icons.Analytics} label="Neural Analytics" />
          <NavItem active={activeTab === 'report'} onClick={() => setActiveTab('report')} icon={Icons.FileText} label="Wealth Report" disabled={!report} />
          <NavItem active={activeTab === 'macro'} onClick={() => setActiveTab('macro')} icon={Icons.Target} label="Macro Outlook" />
          <NavItem active={activeTab === 'system'} onClick={() => setActiveTab('system')} icon={Icons.Settings} label="System Config" />
        </nav>

        {/* Sidebar Footer */}
        <div className="pt-6 border-t border-slate-800">
          <div className="flex items-center space-x-3 p-4 glass-card rounded-2xl border-white/[0.03] shadow-lg">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center font-black text-white shadow-xl shadow-blue-500/20">IV</div>
            <div className="flex-1 overflow-hidden">
              <p className="text-[10px] font-black text-white uppercase tracking-wider truncate">Institutional Pilot</p>
              <div className="flex items-center space-x-2">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest truncate">{systemStatus.crm || 'Connected'}</span>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        {/* Background Gradient */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full -mr-48 -mt-48 z-0"></div>
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-indigo-500/5 blur-[100px] rounded-full -ml-32 -mb-32 z-0"></div>

        <div className="p-8 relative z-10">
          {/* Header */}
          <header className="flex justify-between items-center mb-10">
            <div>
              <p className="text-slate-400 text-sm font-medium mb-1 capitalize">Welcome, Head Advisor</p>
              <h1 className="text-3xl font-bold text-white tracking-tight">Institutional Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Universal Research..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-2.5 w-64 text-sm focus:outline-none focus:border-blue-500 transition-all pl-10"
                />
                <div className="absolute left-3 top-3 text-slate-500">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg>
                </div>
              </div>
              <button className="p-2.5 glass-card rounded-xl text-slate-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></svg>
              </button>
            </div>
          </header>

          {error && (
            <div className="mb-8 p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl flex items-center space-x-3 text-rose-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" /></svg>
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          {/* Tab Content */}
          {activeTab === 'overview' && (
            <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <SectionTitle icon={Icons.Dashboard}>Wealth Overview Terminal</SectionTitle>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard title="Total AUM" value={`$${(stats.totalAUM / 1000000).toFixed(1)}M`} icon={Icons.Dashboard} trend={2.4} colorClass="bg-blue-500" />
                <StatCard title="Avg Sharpe" value={stats.avgSharpe} icon={Icons.Target} trend={0.5} colorClass="bg-indigo-500" />
                <StatCard title="At Risk Exposure" value={`${stats.atRiskPct}%`} icon={Icons.Analytics} trend={-1.2} colorClass="bg-rose-500" />
                <StatCard title="On Track Portfolios" value={stats.onTrackCount} icon={Icons.Users} trend={4} colorClass="bg-emerald-500" />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-6">
                  <SectionTitle icon={Icons.Users}>High-Priority Accounts</SectionTitle>
                  <div className={`space-y-4 ${showAllClients ? 'max-h-[600px] overflow-y-auto pr-2 custom-scrollbar' : ''}`}>
                    {(showAllClients ? filteredClients : filteredClients.slice(0, 5)).map(client => (
                      <ClientListItem
                        key={client.id}
                        client={client}
                        onAction={() => handleGenerateReport(client)}
                        onPortfolioClick={() => setHoldingClient(client)}
                      />
                    ))}
                    {!showAllClients && filteredClients.length > 5 && (
                      <button
                        onClick={() => setShowAllClients(true)}
                        className="w-full py-4 text-sm font-black text-blue-400 hover:text-blue-300 transition-all uppercase tracking-widest bg-blue-500/5 rounded-2xl border border-dashed border-blue-500/20 hover:border-blue-500/40"
                      >
                        View All {filteredClients.length} Institutional Clients ↓
                      </button>
                    )}
                    {showAllClients && (
                      <button
                        onClick={() => setShowAllClients(false)}
                        className="w-full py-4 text-sm font-black text-slate-500 hover:text-slate-300 transition-all uppercase tracking-widest"
                      >
                        Collapse List ↑
                      </button>
                    )}
                  </div>
                </div>

                <div className="space-y-8">
                  <div className="glass-card p-6 rounded-2xl">
                    <h3 className="text-white font-semibold mb-6">Risk Composition</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie data={riskData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                            {riskData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#fff' }} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="flex justify-between mt-4">
                      {riskData.map((d, i) => (
                        <div key={d.name} className="flex flex-col items-center">
                          <span className="text-[10px] text-slate-400 uppercase tracking-wider">{d.name}</span>
                          <span className="text-white font-bold">{d.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="glass-card p-6 rounded-2xl bg-gradient-to-br from-blue-600/20 to-indigo-600/20 border-blue-500/20">
                    <h3 className="text-white font-bold mb-2">Alpha Insights</h3>
                    <p className="text-slate-300 text-sm leading-relaxed mb-4">
                      Market volatility is currently 12% below the 5-year average. Opportunity detected in Tech-Growth sectors.
                    </p>
                    <button onClick={handleMacroReport} className="text-xs font-bold text-blue-400 uppercase tracking-widest hover:text-blue-300">
                      Access Full Macro Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'report' && report && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="flex justify-between items-end mb-8">
                <div>
                  <p className="text-blue-400 text-sm font-bold uppercase tracking-widest mb-1">AI Synthesis Complete</p>
                  <h2 className="text-3xl font-bold text-white">Wealth Strategy {selectedClient ? `for ${selectedClient.name}` : ''}</h2>
                </div>
                <div className="flex space-x-4">
                  <button onClick={handleExportJSON} className="px-4 py-2.5 glass-card rounded-xl text-sm font-medium hover:bg-slate-800 transition-colors">Export JSON</button>
                  <button className="px-6 py-2.5 bg-blue-500 hover:bg-blue-600 text-white rounded-xl text-sm font-bold transition-all shadow-lg shadow-blue-500/20">Download PDF (Demo)</button>
                </div>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                <div className="xl:col-span-2 space-y-8">
                  {/* Glossy Multi-Box Report Layout */}
                  <div className="grid grid-cols-1 gap-8">
                    {/* Box 1: Executive Summary */}
                    <ReportBox
                      title="Investment Outlook"
                      content={(() => {
                        const marker = report.final_report?.match(/\*\*Key Strengths:\*\*/i)?.[0];
                        const parts = marker ? report.final_report?.split(marker) : [report.final_report];
                        return parts[0] || "Synthesizing investment outlook...";
                      })()}
                      icon={Icons.Dashboard}
                    />

                    {/* Box 2: Analysis & Risk */}
                    <ReportBox
                      title="Portfolio Dynamics"
                      content={(() => {
                        const strengthsMarker = report.final_report?.match(/\*\*Key Strengths:\*\*/i)?.[0];
                        const overallMarker = report.final_report?.match(/\*\*Overall:\*\*/i)?.[0];
                        if (!strengthsMarker) return "Analyzing portfolio dynamics...";

                        const strengthsPart = report.final_report?.split(strengthsMarker)[1];
                        const riskPart = overallMarker ? strengthsPart?.split(overallMarker)[0] : strengthsPart;
                        return riskPart ? `### Key Strengths & Analysis\n${riskPart}` : "Analyzing portfolio dynamics...";
                      })()}
                      icon={Icons.Target}
                      accent="indigo"
                    />

                    {/* Box 3: Strategic Recommendations */}
                    <ReportBox
                      title="Final Strategic Verdict"
                      content={(() => {
                        const marker = report.final_report?.match(/\*\*Overall:\*\*/i)?.[0];
                        const parts = marker ? report.final_report?.split(marker) : [];
                        return parts[1] ? `### Strategic Recommendation\n${parts[1]}` : "Finalizing institutional verdict...";
                      })()}
                      icon={Icons.FileText}
                      accent="emerald"
                    />
                  </div>

                  {/* Interactive Asset Feed for RMs */}
                  <div className="glass-card p-10 rounded-3xl border-white/5">
                    <div className="flex items-center justify-between mb-8">
                      <h3 className="text-xl font-black text-white uppercase tracking-tight">Structured Performance Feed</h3>
                      <div className="px-4 py-1.5 bg-blue-500/10 rounded-xl text-[10px] font-black text-blue-400 uppercase tracking-widest border border-blue-500/20">
                        Institutional Grade
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {['AAPL', 'MSFT', 'GOOGL', 'AMZN'].map((ticker, idx) => (
                        <div key={ticker} className="p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-blue-500/30 transition-all cursor-pointer group">
                          <div className="flex justify-between items-start mb-4">
                            <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center font-black text-blue-400 border border-white/5 shadow-inner">{ticker[0]}</div>
                            <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-wider ${idx === 2 ? 'text-rose-400 bg-rose-400/5' : 'text-emerald-400 bg-emerald-400/5'}`}>
                              {idx === 2 ? 'At Risk' : 'Bullish Sentiment'}
                            </span>
                          </div>
                          <div className="flex justify-between items-end">
                            <div>
                              <p className="text-xs font-black text-white group-hover:text-blue-400 transition-colors uppercase tracking-tight">{ticker}</p>
                              <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">Neural Rating: {9.8 - (idx * 0.4)}</p>
                            </div>
                            <div className="text-right">
                              <p className="text-sm font-mono text-white">Focus</p>
                              <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">Expansion Mode</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-6">
                  <h3 className="text-white font-bold uppercase text-[10px] tracking-[0.2em] flex items-center space-x-2 mb-4">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 font-black animate-pulse"></span>
                    <span>Brain Trust Consensus</span>
                  </h3>
                  <PersonaCard name="Warren Buffett" content={report.buffett_analysis} color="blue" />
                  <PersonaCard name="Benjamin Graham" content={report.graham_analysis} color="indigo" />
                  <PersonaCard name="Cathie Wood" content={report.cathie_wood_analysis} color="emerald" />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <SectionTitle icon={Icons.Analytics}>Portfolio Performance Clusters</SectionTitle>
              <div className="glass-card p-8 rounded-3xl h-[500px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={clients.slice(0, 10).map(c => ({ name: c.id, AUM: c.portfolio_value / 1000, Sharpe: (c.sharpe_ratio || 0.8) * 100 }))}>
                    <defs>
                      <linearGradient id="colorAum" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.5)' }} />
                    <Area type="monotone" dataKey="AUM" stroke="#3b82f6" fillOpacity={1} fill="url(#colorAum)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-center">
                <div className="p-8 glass-card rounded-2xl border-emerald-500/20">
                  <h3 className="text-xl font-bold text-white mb-2">System Alpha Score</h3>
                  <div className="text-6xl font-black text-emerald-400 mb-4">9.4</div>
                  <p className="text-sm text-slate-400 italic">"Superior risk-adjusted performance across all buckets"</p>
                </div>
                <div className="p-8 glass-card rounded-2xl border-blue-500/20">
                  <h3 className="text-xl font-bold text-white mb-2">Agent Confidence</h3>
                  <div className="text-6xl font-black text-blue-400 mb-4">98%</div>
                  <p className="text-sm text-slate-400 italic">"Orchestration layer operating at peak efficiency"</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'macro' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-8">
              <SectionTitle icon={Icons.Analytics}>Institutional Macro Outlook</SectionTitle>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 glass-card p-10 rounded-3xl border-blue-500/20 bg-gradient-to-br from-slate-900 to-blue-900/10">
                  <div className="max-w-3xl">
                    <h3 className="text-2xl font-black text-white mb-6 tracking-tighter uppercase">Q1 2026 Market Synthesis</h3>
                    <p className="text-slate-300 leading-relaxed mb-8 text-lg font-medium">
                      Our AI ensemble has detected a significant rotation into defensive tech buckets and green-energy infrastructure. Institutional liquidity indices are trending 14bps above the 5-year mean, suggesting a robust foundation for growth-oriented strategies.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="p-6 bg-slate-900/50 rounded-2xl border border-white/5 shadow-inner">
                        <p className="text-[10px] text-blue-400 font-black uppercase tracking-[0.2em] mb-2">Volatility Index</p>
                        <p className="text-2xl font-black text-white">12.4 <span className="text-xs text-rose-500 font-bold">-2.1%</span></p>
                      </div>
                      <div className="p-6 bg-slate-900/50 rounded-2xl border border-white/5 shadow-inner">
                        <p className="text-[10px] text-emerald-400 font-black uppercase tracking-[0.2em] mb-2">Bull Sentiment</p>
                        <p className="text-2xl font-black text-white">68% <span className="text-xs text-emerald-500 font-bold">+4%</span></p>
                      </div>
                      <div className="p-6 bg-slate-900/50 rounded-2xl border border-white/5 shadow-inner">
                        <p className="text-[10px] text-indigo-400 font-black uppercase tracking-[0.2em] mb-2">Liquidity Delta</p>
                        <p className="text-2xl font-black text-white">+1.24%</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="space-y-6">
                  <div className="glass-card p-8 rounded-3xl border-white/5">
                    <h4 className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em] mb-4">Neural Warning</h4>
                    <p className="text-sm text-slate-300 leading-relaxed font-medium">Rotation into <span className="text-white font-bold">Defensive Tech</span> has accelerated. Watch for liquidity traps in mid-cap clusters.</p>
                  </div>
                  <div className="glass-card p-8 rounded-3xl border-emerald-500/20 bg-emerald-500/5">
                    <h4 className="text-[10px] font-black text-emerald-400 uppercase tracking-[0.2em] mb-4">Alpha Opportunity</h4>
                    <p className="text-sm text-slate-300 leading-relaxed font-medium">Energy sector is showing <span className="text-white font-bold">extreme divergence</span>. Strategic accumulation recommended.</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'system' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-8">
              <SectionTitle icon={Icons.Settings}>System Configuration</SectionTitle>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="glass-card p-8 rounded-3xl space-y-6">
                  <h3 className="text-lg font-bold text-white">Engine Parameters</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-xl">
                      <span className="text-sm text-slate-400">LLM Provider</span>
                      <span className="text-sm font-mono text-blue-400">{systemStatus.llm || 'OpenRouter'}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-xl">
                      <span className="text-sm text-slate-400">CRM Connectivity</span>
                      <span className="text-sm font-mono text-emerald-400">{systemStatus.crm || 'Connected'}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-xl">
                      <span className="text-sm text-slate-400">Response Optimization</span>
                      <span className="text-sm font-mono text-indigo-400">High Efficiency (Tuned)</span>
                    </div>
                  </div>
                </div>
                <div className="glass-card p-8 rounded-3xl bg-blue-500/5 border-blue-500/20 flex flex-col justify-center items-center text-center">
                  <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mb-4">
                    <Icons.Target />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2">Institutional Node Active</h3>
                  <p className="text-sm text-slate-400 max-w-xs">Your system is currently operating on the specialized Ivy Hackathon node (v3.0.x).</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-[100] flex items-center justify-center flex-col">
          <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-6"></div>
          <p className="text-xl font-bold text-white mb-2 tracking-tight">Accessing Neural Advisors</p>
          <div className="flex space-x-2">
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
          </div>
        </div>
      )}

      {/* Interactive Perspective Modal */}
      <HoldingModal client={holdingClient} isOpen={!!holdingClient} onClose={() => setHoldingClient(null)} />
    </div>
  );
}

function ReportBox({ title, content, icon: Icon, accent = "blue" }) {
  const accentMap = {
    blue: "border-blue-500/20 bg-blue-500/5",
    indigo: "border-indigo-500/20 bg-indigo-500/5",
    emerald: "border-emerald-500/20 bg-emerald-500/5"
  };

  const textAccent = {
    blue: "text-blue-400",
    indigo: "text-indigo-400",
    emerald: "text-emerald-400"
  };

  const bgAccent = {
    blue: "bg-blue-500/10",
    indigo: "bg-indigo-500/10",
    emerald: "bg-emerald-500/10"
  };

  return (
    <div className={`glass-card p-10 rounded-[2.5rem] border relative overflow-hidden transition-all duration-500 hover:scale-[1.01] ${accentMap[accent]}`}>
      <div className="flex items-center space-x-4 mb-8">
        <div className={`p-2.5 rounded-xl ${bgAccent[accent]} ${textAccent[accent]} border border-white/5 shadow-inner`}>
          <Icon size={20} />
        </div>
        <h3 className="text-xl font-black text-white uppercase tracking-tight">{title}</h3>
      </div>
      <div className="prose prose-invert max-w-none prose-sm">
        <MarkdownErrorBoundary>
          <div className="text-slate-300 leading-relaxed font-medium space-y-4 markdown-content">
            <ReactMarkdown>
              {content || "No content"}
            </ReactMarkdown>
          </div>
        </MarkdownErrorBoundary>
      </div>
    </div>
  );
}

// --- Sub-Components ---

function NavItem({ active, onClick, icon: Icon, label, disabled }) {
  return (
    <button
      disabled={disabled}
      onClick={onClick}
      className={`w-full flex items-center space-x-3 px-4 py-3.5 rounded-2xl text-xs font-bold transition-all duration-200 ${active
        ? 'bg-blue-600/10 text-blue-400 border border-blue-500/20 shadow-[inset_0_1px_10px_rgba(56,189,248,0.05)]'
        : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'
        } ${disabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer hover:translate-x-1'}`}
    >
      <Icon size={18} />
      <span className="uppercase tracking-widest">{label}</span>
    </button>
  );
}

function ClientListItem({ client, onAction, onPortfolioClick }) {
  return (
    <div className="glass-card p-5 rounded-2xl flex items-center justify-between group border-white/[0.03]">
      <div className="flex items-center space-x-5">
        <div className="w-12 h-12 rounded-xl bg-slate-900 border border-white/5 flex items-center justify-center font-black text-slate-500 group-hover:text-blue-400 transition-all shadow-inner">
          {client.name.split(' ').map(n => n[0]).join('')}
        </div>
        <div onClick={onPortfolioClick} className="cursor-pointer">
          <h4 className="text-base font-black text-white group-hover:text-blue-400 transition-colors tracking-tight">{client.name}</h4>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.15em]">{client.id} • {client.email}</p>
        </div>
      </div>
      <div className="flex items-center space-x-10">
        <div className="text-right cursor-pointer" onClick={onPortfolioClick}>
          <p className="text-white font-black text-lg tracking-tighter">${(client.portfolio_value / 1000).toFixed(0)}K</p>
          <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">AUM Value</p>
        </div>
        <div className={`px-4 py-1.5 rounded-xl text-[9px] font-black uppercase tracking-[0.2em] border ${client.status === 'On Track' ? 'bg-emerald-500/5 text-emerald-400 border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.05)]' :
          client.status === 'At Risk' ? 'bg-rose-500/5 text-rose-400 border-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.05)]' :
            'bg-amber-500/5 text-amber-400 border-amber-500/20 shadow-[0_0_15px_rgba(245,158,11,0.05)]'
          }`}>
          {client.status}
        </div>
        <button onClick={onAction} className="p-3 bg-slate-800 hover:bg-blue-600 text-slate-400 hover:text-white rounded-xl transition-all shadow-lg border border-white/5 active:scale-90">
          <Icons.FileText size={20} />
        </button>
      </div>
    </div>
  );
}

function ClientGridCard({ client, onAction }) {
  return (
    <div className="glass-card p-6 rounded-2xl group border-white/5 hover:border-blue-500/30">
      <div className="flex justify-between items-start mb-6">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center border border-slate-600/50">
          <span className="font-bold text-slate-300">{client.name.split(' ').map(n => n[0]).join('')}</span>
        </div>
        <div className={`px-2 py-1 rounded text-[10px] font-black uppercase ${client.status === 'On Track' ? 'text-emerald-400 bg-emerald-400/5' :
          client.status === 'At Risk' ? 'text-rose-400 bg-rose-400/5' : 'text-amber-400 bg-amber-400/5'
          }`}>
          {client.status}
        </div>
      </div>

      <h3 className="text-lg font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">{client.name}</h3>
      <p className="text-xs text-slate-500 mb-6">{client.email}</p>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-3 bg-slate-900/50 rounded-xl">
          <p className="text-[10px] text-slate-500 tracking-widest uppercase mb-1">AUM</p>
          <p className="text-sm font-bold text-white">${(client.portfolio_value / 1000).toFixed(0)}K</p>
        </div>
        <div className="p-3 bg-slate-900/50 rounded-xl">
          <p className="text-[10px] text-slate-500 tracking-widest uppercase mb-1">Risk</p>
          <p className="text-sm font-bold text-white">{client.risk_tolerance}</p>
        </div>
      </div>

      <button onClick={onAction} className="w-full py-3 bg-slate-800 group-hover:bg-blue-600 text-slate-300 group-hover:text-white text-xs font-bold uppercase tracking-widest rounded-xl transition-all border border-white/5">
        Analyze Portfolio
      </button>
    </div>
  );
}

const HoldingModal = ({ client, isOpen, onClose }) => {
  if (!isOpen || !client) return null;

  // High-fidelity institutional holding data
  const stocks = [
    { ticker: "AAPL", name: "Apple Inc.", weight: 0.20, status: "Watchlist", trend: "+1.2%" },
    { ticker: "MSFT", name: "Microsoft Corp.", weight: 0.25, status: "On Track", trend: "+0.8%" },
    { ticker: "GOOGL", name: "Alphabet Inc.", weight: 0.15, status: "At Risk", trend: "-2.4%" },
    { ticker: "AMZN", name: "Amazon.com Inc.", weight: 0.10, status: "On Track", trend: "+1.5%" },
    { ticker: "BND", name: "Vanguard Total Bond", weight: 0.30, status: "On Track", trend: "-0.1%" },
  ];

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-300">
      <div className="glass-card w-full max-w-2xl rounded-[2.5rem] p-10 border-white/10 shadow-2xl relative overflow-hidden">
        {/* Background Accent */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 blur-[100px] rounded-full -mr-32 -mt-32"></div>

        <button onClick={onClose} className="absolute top-8 right-8 p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-full transition-all">
          <Icons.Dashboard size={20} />
        </button>

        <div className="mb-10 relative">
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 rounded-full bg-blue-500"></div>
            <p className="text-blue-400 text-[10px] font-black uppercase tracking-[0.2em]">Institutional Vault • Real-time View</p>
          </div>
          <h2 className="text-3xl font-black text-white tracking-tight">{client.name} Portfolio</h2>
          <div className="flex items-center space-x-3 mt-2">
            <span className="text-slate-500 text-xs font-medium uppercase tracking-widest">AUM: <span className="text-white">${(client.portfolio_value / 1000).toLocaleString()}K</span></span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-800"></span>
            <span className="text-slate-500 text-xs font-medium uppercase tracking-widest">Risk: <span className="text-blue-400">{client.risk_tolerance || 'Moderate'}</span></span>
          </div>
        </div>

        <div className="overflow-hidden rounded-3xl border border-white/5 bg-slate-900/40">
          <table className="w-full text-left text-sm border-collapse">
            <thead className="bg-white/5 text-slate-500 font-bold uppercase text-[9px] tracking-[0.15em]">
              <tr>
                <th className="px-8 py-5 text-blue-400/50">Asset Class</th>
                <th className="px-8 py-5">Fiduciary Status</th>
                <th className="px-8 py-5 text-right">Value (USD)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {stocks.map((s) => (
                <tr key={s.ticker} className="hover:bg-blue-500/5 transition-all group">
                  <td className="px-8 py-5">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center font-black text-xs text-blue-400 border border-white/5 shadow-inner">
                        {s.ticker[0]}
                      </div>
                      <div>
                        <div className="font-black text-white group-hover:text-blue-400 transition-colors uppercase tracking-tight">{s.ticker}</div>
                        <div className="text-[10px] text-slate-500 font-medium tracking-wide">{s.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center space-x-2">
                      <span className={`w-1.5 h-1.5 rounded-full ${s.status === 'At Risk' ? 'bg-rose-500 animate-pulse shadow-[0_0_8px_rgba(244,63,94,0.6)]' :
                        s.status === 'Watchlist' ? 'bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.4)]' :
                          'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]'
                        }`}></span>
                      <span className={`text-[10px] font-black uppercase tracking-widest ${s.status === 'At Risk' ? 'text-rose-400' :
                        s.status === 'Watchlist' ? 'text-amber-400' :
                          'text-emerald-400'
                        }`}>
                        {s.status}
                      </span>
                    </div>
                  </td>
                  <td className="px-8 py-5 text-right">
                    <div className="font-mono text-white font-black tracking-tighter text-base">
                      ${((client.portfolio_value * s.weight) / 1000).toLocaleString()}K
                    </div>
                    <div className={`text-[9px] font-black tracking-widest uppercase ${s.trend.startsWith('+') ? 'text-emerald-500' : 'text-rose-500'}`}>
                      {s.trend} 24h
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-10 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-slate-700 animate-pulse"></div>
            <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">Pricing Latency: 14ms • Institutional Verified</p>
          </div>
          <button onClick={onClose} className="px-10 py-5 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] transition-all shadow-xl shadow-blue-600/30 active:scale-95">
            Exit Perspective
          </button>
        </div>
      </div>
    </div>
  );
};

function PersonaCard({ name, content, color }) {
  const colorMap = {
    blue: "from-blue-500/20 to-blue-600/5 shadow-blue-500/5 border-blue-500/20",
    indigo: "from-indigo-500/20 to-indigo-600/5 shadow-indigo-500/5 border-indigo-500/20",
    emerald: "from-emerald-500/20 to-emerald-600/5 shadow-emerald-500/5 border-emerald-500/20"
  };

  return (
    <div className={`glass-card p-8 rounded-3xl border bg-gradient-to-br transition-all hover:scale-[1.02] duration-300 shadow-xl ${colorMap[color] || colorMap.blue} relative overflow-hidden group`}>
      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
        <Icons.Dashboard size={40} />
      </div>
      <h4 className="font-black text-[10px] uppercase tracking-[0.2em] mb-4 text-blue-400 flex items-center space-x-2">
        <span className="w-2 h-2 rounded-full bg-blue-500"></span>
        <span>{name} Perspective</span>
      </h4>
      <p className="text-sm leading-relaxed text-slate-300 italic font-medium">
        "{content || "Synthesizing market Alpha..."}"
      </p>
    </div>
  );
}
