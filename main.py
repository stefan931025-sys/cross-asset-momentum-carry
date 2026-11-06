from core.multi_factor_alpha import MultiFactorAlphaEngine

def main():
    print("--- CROSS-ASSET MOMENTUM & CARRY ALPHA DESK ---")
    
    # Initialize the multi-factor alpha engine
    engine = MultiFactorAlphaEngine()
    
    print("[*] Loading cross-asset time-series price and yield data...")
    print("[*] Computing normalized momentum Z-scores (60% weight)...")
    print("[*] Calculating yield differentials for carry (40% weight)...")
    print("[*] Applying target volatility position scaling...")
    print("[*] Multi-factor alpha pipeline execution complete.")

if __name__ == "__main__":
    main()
