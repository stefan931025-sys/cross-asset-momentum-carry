"""
Main Script: main.py
Description: Execution pipeline for the Cross-Asset Momentum & Carry Strategy Engine,
incorporating HMM macro regime overlay, dynamic volatility scaling, and stress testing.
"""

import numpy as np
import pandas as pd
from core.macro_overlay import MacroRegimeOverlay, StressTestingModule

class CrossAssetMomentumCarryEngine:
    """
    Institutional multi-asset factor investing framework capturing trend persistence
    and yield differentials with dynamic macro-regime conditioning.
    """
    def __init__(self, target_volatility: float = 0.10):
        self.macro_overlay = MacroRegimeOverlay(n_states=3)
        self.stress_module = StressTestingModule(target_volatility=target_volatility)
        
    def generate_signal_weights(self, price_data: pd.DataFrame, carry_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculates raw time-series momentum, cross-sectional momentum, and carry factor weights.
        """
        # 1. Time-Series Momentum (TSMOM) - 12-month lookback excluding recent month
        ts_mom = price_data.shift(21).pct_change(252 - 21)
        ts_mom_weights = np.sign(ts_mom)
        
        # 2. Cross-Sectional Momentum (XSMOM) - Ranking cross-sectional returns over 6 months
        cs_returns = price_data.pct_change(126)
        cs_ranks = cs_returns.rank(axis=1, pct=True) - 0.5
        cs_mom_weights = cs_ranks.div(cs_ranks.abs().sum(axis=1), axis=0).fillna(0)
        
        # Combine momentum signals
        combined_momentum = 0.5 * ts_mom_weights.fillna(0) + 0.5 * cs_mom_weights
        
        # 3. Carry Factor - Yield/Roll differentials normalized cross-sectionally
        carry_weights = carry_data.rank(axis=1, pct=True) - 0.5
        carry_weights = carry_weights.div(carry_weights.abs().sum(axis=1), axis=0).fillna(0)
        
        return combined_momentum, carry_weights

    def run_backtest(self, price_data: pd.DataFrame, carry_data: pd.DataFrame, macro_features: pd.DataFrame) -> dict:
        """
        Executes full strategy backtest incorporating macro regime conditioning and risk scaling.
        """
        print("Initializing Cross-Asset Momentum & Carry Strategy Backtest...")
        
        # Fit HMM and predict macro regimes from feature matrix
        regime_states = self.macro_overlay.fit_predict_regimes(macro_features)
        
        # Generate raw factor weights
        momentum_w, carry_w = self.generate_signal_weights(price_data, carry_data)
        
        burn_in = 252
        portfolio_returns = pd.Series(index=price_data.index[burn_in:], dtype=float)
        weights_history = []
        
        for i in range(burn_in, len(price_data)):
            current_regime = regime_states[i] if i < len(regime_states) else regime_states[-1]
            
            # Slice current factor weights
            curr_mom = momentum_w.iloc[i]
            curr_carry = carry_w.iloc[i]
            
            # Apply regime-conditioned dynamic tilt (dampening risk during slowdowns/crises)
            adjusted_weights = self.macro_overlay.compute_dynamic_tilt(
                regime_state=current_regime,
                momentum_weights=curr_mom,
                carry_weights=curr_carry
            )
            
            # Apply rolling volatility scaling to maintain target portfolio risk budget
            if i > burn_in + 63:
                hist_ret = portfolio_returns.iloc[max(0, (i - burn_in) - 63):(i - burn_in)]
                scaling_factor = self.stress_module.volatility_scaling(hist_ret).iloc[-1]
                if pd.isna(scaling_factor):
                    scaling_factor = 1.0
            else:
                scaling_factor = 1.0
                
            final_weights = adjusted_weights * scaling_factor
            weights_history.append(final_weights)
            
            # Compute daily asset returns and portfolio return
            asset_returns = price_data.pct_change().iloc[i]
            port_ret = np.dot(final_weights.fillna(0), asset_returns.fillna(0))
            portfolio_returns.iloc[i - burn_in] = port_ret

        portfolio_returns = portfolio_returns.dropna()
        
        # Simulate historical left-tail shock scenario (e.g., COVID-19 liquidity shock)
        stressed_returns = self.stress_module.simulate_historical_stress(portfolio_returns, shock_scenario="COVID_2020")
        
        return {
            "portfolio_returns": portfolio_returns,
            "stressed_returns": stressed_returns,
            "weights_history": pd.DataFrame(weights_history, index=price_data.index[burn_in:])
        }

if __name__ == "__main__":
    # Standalone validation harness
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=750, freq="B")
    assets = ["Equities_Global", "US_Treasuries", "FX_G10", "Commodities_Broad"]
    
    price_df = pd.DataFrame(100 * (1 + np.random.normal(0.0004, 0.012, size=(750, len(assets)))), index=dates, columns=assets).cumprod()
    carry_df = pd.DataFrame(np.random.normal(0.015, 0.004, size=(750, len(assets))), index=dates, columns=assets)
    macro_df = pd.DataFrame(np.random.normal(0, 1, size=(750, 3)), index=dates, columns=["TermSpread", "GrowthSurprise", "InflationMom"])
    
    engine = CrossAssetMomentumCarryEngine(target_volatility=0.10)
    results = engine.run_backtest(price_df, carry_df, macro_df)
    
    print("Execution Pipeline Complete.")
    print(f"Annualized Realized Return: {results['portfolio_returns'].mean() * 252:.2%}")
    print(f"Annualized Realized Volatility: {results['portfolio_returns'].std() * np.sqrt(252):.2%}")
    print(f"Max Stressed Drawdown (COVID Scenario): {results['stressed_returns'].min():.2%}")
