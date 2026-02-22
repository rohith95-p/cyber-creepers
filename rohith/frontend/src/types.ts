export interface FinalState {
  client_id?: string;
  portfolio_assets?: Array<{ ticker: string; quantity: number; asset_type: string }>;
  market_data?: Record<string, Array<{ date: string; close: number; high?: number; low?: number }>>;
  risk_metrics?: {
    cvar_95?: number;
    max_drawdown?: number;
    sharpe_ratio?: number;
    monte_carlo?: {
      prob_of_gain_1yr?: number;
      median_outcome?: number;
      worst_5pct?: number;
      best_5pct?: number;
      simulation_paths?: number;
      projection_days?: number;
    };
  };
  final_report?: string;
  compliance_status?: string;
  client_profile?: Record<string, unknown>;
  buffett_analysis?: string;
  graham_analysis?: string;
  cathie_wood_analysis?: string;
  goal_planning_analysis?: string;
}
