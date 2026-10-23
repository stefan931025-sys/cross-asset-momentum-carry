import pytest

def test_multi_factor_alpha_score():
    """Verify combined score calculation using 60% momentum and 40% carry weights."""
    momentum_zscore = 1.5
    carry_zscore = 0.5
    
    momentum_weight = 0.60
    carry_weight = 0.40
    
    combined_alpha = (momentum_zscore * momentum_weight) + (carry_zscore * carry_weight)
    
    assert pytest.approx(combined_alpha, 0.001) == 1.10

def test_volatility_targeting_scaler():
    """Verify leverage/position scaling factor relative to target portfolio volatility."""
    target_vol = 0.10      # 10% target annualized volatility
    realized_vol = 0.20    # 20% realized volatility (high volatility environment)
    
    vol_scaler = target_vol / realized_vol
    
    assert pytest.approx(vol_scaler, 0.01) == 0.50  # De-leverage position by 50%
