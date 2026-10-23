![CI Pipeline](https://github.com/stefan931025-sys/cross-asset-momentum-carry/actions/workflows/ci.yml/badge.svg)

# Cross-Asset Momentum & Carry Alpha Engine[span_5](start_span)[span_5](end_span)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description[span_6](start_span)[span_6](end_span)
Systematic multi-factor alpha generation engine combining time-series momentum, carry yield differentials, and target volatility position scaling across liquid asset classes[span_7](start_span)[span_7](end_span).

---

## 📌 Strategy Design[span_8](start_span)[span_8](end_span)

* **Multi-Factor Alpha Construction:** Combines normalized momentum Z-scores (60% weight) and yield carry differentials (40% weight)[span_9](start_span)[span_9](end_span).
* **Volatility Targeting:** Dynamically scales leverage and position sizes based on rolling annualized asset volatility relative to portfolio target risk[span_10](start_span)[span_10](end_span).
* **Risk Controls:** Enforces hard caps on leverage and drawdown parameters[span_11](start_span)[span_11](end_span).

---

## 🚀 Quickstart[span_12](start_span)[span_12](end_span)

```bash
# Clone repository
git clone [https://github.com/stefan931025-sys/cross-asset-momentum-carry.git](https://github.com/stefan931025-sys/cross-asset-momentum-carry.git)
cd cross-asset-momentum-carry

# Run multi-factor alpha engine from src directory
python src/multi_factor_alpha.py
