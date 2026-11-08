"""
Module: core/macro_overlay.py
Description: Macroeconomic Regime Classifier and Risk-Scaling Overlay for Cross-Asset Momentum & Carry Engine.
"""

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler

class MacroRegimeOverlay:
    """
    Classifies macroeconomic regimes using rolling indicators and adjusts factor weights
    dynamically to mitigate drawdowns during liquidity crunches or high-inflation shocks.
    """
    def __init__(self, n_states: int = 3, covariance_type: str = "full"):
        self.n_states = n_states
        self.model = GaussianHMM(n_components=n_states, covariance_type=covariance_type, n_iter=1000, random_state=42)
        self.scaler = StandardScaler()
        self.regime_labels = {}

    def fit_predict_regimes(self, macro_features: pd.DataFrame) -> np.ndarray:
        """
        Fits a Gaussian HMM on macro features (e.g., term spreads, growth surprises, inflation momentum)
        and predicts historical market regimes.
        """
        scaled_data = self.scaler.fit_transform(macro_features.dropna())
        self.model.fit(scaled_data)
        hidden_states = self.model.predict(scaled_data)
        return hidden_states

    def compute_dynamic_tilt(self, regime_state: int, momentum_weights: pd.Series, carry_weights: pd.Series) -> pd.Series:
        """
        Adjusts factor weights based on the active regime state:
        - State 0 (Expansion): Overweight momentum, normal carry.
        - State 1 (Slowdown / Stagflation): Dampen momentum, reduce carry exposure.
        - State 2 (Liquidity Crisis): Defensive positioning, aggressive risk reduction.
        """
        if regime_state == 0:
            # Expansion: High momentum conviction
            return 1.2 * momentum_weights + 1.0 * carry_weights
        elif regime_state == 1:
            # Slowdown / Stagflation: Dampen momentum, reduce carry
            return 0.5 * momentum_weights + 0.5 * carry_weights
        else:
            # Crisis: Defensive stance, major risk reduction
            return 0.1 * momentum_weights + 0.1 * carry_weights


class StressTestingModule:
    """
    Applies dynamic volatility scaling and simulates historical crisis shock overlays.
    """
    def __init__(self, target_volatility: float = 0.10):
        self.target_volatility = target_volatility

    def volatility_scaling(self, returns: pd.Series, window: int = 63) -> pd.Series:
        """
        Scales positions inversely to realized rolling volatility to maintain a constant risk budget.
        """
        rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)
        scaling_factor = self.target_volatility / rolling_vol.replace(0, np.nan)
        return scaling_factor.clip(upper=3.0)  # Cap leverage multiplier

    def simulate_historical_stress(self, portfolio_returns: pd.Series, shock_scenario: str = "COVID_2020") -> pd.Series:
        """
        Applies historical crisis shock multipliers to evaluate left-tail drawdown profile.
        """
        stress_multipliers = {
            "GFC_2008": 3.5,
            "COVID_2020": 4.0,
            "RATE_SHOCK_2022": 2.5
        }
        multiplier = stress_multipliers.get(shock_scenario, 1.0)
        return portfolio_returns * multiplier
