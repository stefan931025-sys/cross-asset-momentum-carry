import argparse
import numpy as np
import pandas as pd
import yfinance as yf

class MultiFactorAlphaEngine:
    """
    Live Multi-Factor Cross-Asset Momentum & Carry Strategy Engine.
    """
    def __init__(self, ticker: str = "SPY"):
        self.ticker = ticker

    def run_factor_strategy(self, target_volatility: float = 0.12, carry_yield: float = 0.04) -> dict:
        data = yf.download(self.ticker, period="1y", progress=False)['Close']
        if data.empty:
            raise ValueError(f"No price data found for {self.ticker}")

        returns = data.pct_change().dropna()
        
        # Momentum Z-score (21-day momentum)
        mom_21 = (data.iloc[-1] - data.iloc[-22]) / data.iloc[-22]
        rolling_mom = (data - data.shift(21)) / data.shift(21)
        mom_zscore = float((mom_21 - rolling_mom.mean()) / rolling_mom.std())

        # Carry Z-score scaling
        carry_zscore = float(np.clip(carry_yield * 10, -3.0, 3.0))

        # Composite Alpha
        composite_alpha = (0.6 * mom_zscore) + (0.4 * carry_zscore)

        # Volatility Targeting Position Sizing
        ann_vol = float(returns.tail(30).std() * np.sqrt(252))
        vol_scalar = target_volatility / ann_vol if ann_vol > 0 else 0.0
        target_weight = np.clip(composite_alpha * vol_scalar, -1.0, 1.0)

        return {
            "Ticker": self.ticker,
            "Momentum_ZScore": round(mom_zscore, 2),
            "Carry_Yield_Assumed": f"{carry_yield:.2%}",
            "Composite_Alpha": round(composite_alpha, 2),
            "Realized_30D_Vol": f"{ann_vol:.2%}",
            "Target_Portfolio_Vol": f"{target_volatility:.0%}",
            "Target_Position_Weight": f"{target_weight:.2%}"
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-Asset Momentum & Carry Alpha Engine")
    parser.add_argument("--ticker", type=str, default="SPY", help="Cross-asset market ticker (e.g. SPY, TLT, GLD)")
    parser.add_argument("--target_vol", type=float, default=0.12, help="Target annualized volatility (e.g. 0.12)")
    args = parser.parse_args()

    engine = MultiFactorAlphaEngine(ticker=args.ticker)
    summary = engine.run_factor_strategy(target_volatility=args.target_vol)

    print("\n================ CROSS-ASSET FACTOR ALPHA PROGRAM ================")
    for k, v in summary.items():
        print(f"{k:<25}: {v}")
    print("===================================================================\n")
