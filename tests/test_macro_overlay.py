"""
Module: tests/test_macro_overlay.py
Description: Pytest unit test suite for MacroRegimeOverlay and StressTestingModule,
verifying state space dimensions, weight bounds, and dynamic volatility scaling safety.
"""

import pytest
import numpy as np
import pandas as pd
from core.macro_overlay import MacroRegimeOverlay, StressTestingModule

@pytest.fixture
def sample_macro_data():
    """Generates synthetic macroeconomic indicator series for regime classification."""
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=250, freq="B")
    data = {
        "TermSpread": np.random.normal(0.5, 0.2, size=250),
        "GrowthSurprise": np.random.normal(0.0, 1.0, size=250),
        "InflationMom": np.random.normal(0.02, 0.005, size=250)
    }
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def sample_factor_weights():
    """Generates sample momentum and carry factor weights across 4 asset classes."""
    assets = ["Equities", "Bonds", "FX", "Commodities"]
    mom_weights = pd.Series([0.4, -0.2, 0.3, 0.1], index=assets)
    carry_weights = pd.Series([0.1, 0.3, -0.1, 0.2], index=assets)
    return mom_weights, carry_weights

def test_hmm_regime_fit_predict(sample_macro_data):
    """Verify that HMM fits successfully and outputs valid state labels within [0, n_states-1]."""
    overlay = MacroRegimeOverlay(n_states=3)
    regimes = overlay.fit_predict_regimes(sample_macro_data)
    
    assert len(regimes) == len(sample_macro_data)
    assert set(np.unique(regimes)).issubset({0, 1, 2})

def test_dynamic_tilt_regimes(sample_factor_weights):
    """Verify factor tilt multipliers under different regime states."""
    mom_w, carry_w = sample_factor_weights
    overlay = MacroRegimeOverlay(n_states=3)
    
    # State 0 (Expansion): 1.2 * Momentum + 1.0 * Carry
    tilt_expansion = overlay.compute_dynamic_tilt(0, mom_w, carry_w)
    expected_expansion = 1.2 * mom_w + 1.0 * carry_w
    pd.testing.assert_series_equal(tilt_expansion, expected_expansion)
    
    # State 2 (Crisis): 0.1 * Momentum + 0.1 * Carry (Defensive risk reduction)
    tilt_crisis = overlay.compute_dynamic_tilt(2, mom_w, carry_w)
    expected_crisis = 0.1 * mom_w + 0.1 * carry_w
    pd.testing.assert_series_equal(tilt_crisis, expected_crisis)

def test_volatility_scaling_bounds():
    """Verify that volatility scaling correctly caps leverage and scales inversely to vol."""
    stress_module = StressTestingModule(target_volatility=0.10)
    
    # Case A: High realized volatility (20%) -> Scaler should de-leverage to 0.5x
    returns_high_vol = pd.Series(np.random.normal(0, 0.20 / np.sqrt(252), size=100))
    scale_high = stress_module.volatility_scaling(returns_high_vol, window=63).iloc[-1]
    assert pytest.approx(scale_high, rel=0.15) == 0.50
    
    # Case B: Ultra-low realized volatility (1%) -> Scaler should cap at 3.0x upper limit
    returns_low_vol = pd.Series(np.random.normal(0, 0.01 / np.sqrt(252), size=100))
    scale_low = stress_module.volatility_scaling(returns_low_vol, window=63).iloc[-1]
    assert scale_low == 3.0

def test_historical_stress_simulation():
    """Verify left-tail shock scenario multiplier application."""
    stress_module = StressTestingModule()
    base_returns = pd.Series([-0.02, 0.01, -0.015])
    
    stressed = stress_module.simulate_historical_stress(base_returns, shock_scenario="COVID_2020")
    pd.testing.assert_series_equal(stressed, base_returns * 4.0)
