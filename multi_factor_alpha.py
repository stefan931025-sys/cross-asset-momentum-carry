import numpy as np
import pandas as pd

class CrossAssetFactorEngine:
    """
    Generates systematic multi-factor (Momentum + Carry) signals with volatility scaling.
    """
    def __init__(self, price_series: pd.Series, yield_differential: float):
        self.prices = price_series
        self.yield_diff = yield_differential  # Annualized carry yield

    def compute_momentum_signal(self, lookback_period: int = 21) -> float:
        returns = self.prices.pct_change(lookback_period).dropna()
        latest_mom = returns.iloc[-1]
        # Normalize to Z-score
        signal = (latest_mom - returns.mean()) / returns.std()
        return np.clip(signal, -3.0, 3.0)

    def compute_target_position(self, target_volatility: float = 0.10) -> dict:
        mom_signal = self.compute_momentum_signal()
        carry_signal = np.clip(self.yield_diff * 10, -3.0, 3.0)  # Scale carry Z-score
        
        composite_alpha = (0.6 * mom_signal) + (0.4 * carry_signal)
        
        # Calculate daily asset volatility
        daily_returns = self.prices.pct_change().dropna()
        annualized_vol = daily_returns.std() * np.sqrt(252)
        
        # Volatility-targeted position sizing
        vol_scalar = target_volatility / annualized_vol if annualized_vol > 0 else 0
        raw_position = composite_alpha * vol_scalar
        final_position = np.clip(raw_position, -1.0, 1.0)  # Cap position leverage

        return {
            "Momentum_ZScore": round(mom_signal, 2),
            "Carry_ZScore": round(carry_signal, 2),
            "Composite_Alpha": round(composite_alpha, 2),
            "Annualized_Vol": f"{annualized_vol:.2%}",
            "Target_Vol": f"{target_volatility:.0%}",
            "Recommended_Position_Weight": f"{final_position:.2%}"
        }

if __name__ == "__main__":
    # Simulate 60 days of daily price data
    np.random.seed(42)
    base_price = 100
    price_path = base_price * np.exp(np.cumsum(np.random.normal(0.0005, 0.012, 60)))
    prices = pd.Series(price_path)

    engine = CrossAssetFactorEngine(price_series=prices, yield_differential=0.035)  # 3.5% carry yield
    allocation = engine.compute_target_position(target_volatility=0.12)

    print("--- Cross-Asset Factor Alpha Engine ---")
    for k, v in allocation.items():
        print(f"{k}: {v}")
