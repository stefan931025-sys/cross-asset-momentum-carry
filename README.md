[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/stefan931025-sys/cross-asset-momentum-carry)

# Cross-Asset Momentum & Carry Alpha Engine

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Description:**  
Systematic multi-factor alpha generation engine combining time-series momentum, carry yield differentials, and target volatility position scaling across liquid asset classes.

---

## 📌 Strategy Design

* **Multi-Factor Alpha Construction:** Combines normalized momentum Z-scores (60% weight) and yield carry differentials (40% weight).
* **Volatility Targeting:** Dynamically scales leverage and position sizes based on rolling annualized asset volatility relative to portfolio target risk.
* **Risk Controls:** Enforces hard caps on leverage and drawdown parameters.

---

## 🛠️ Quickstart

git clone https://github.com/stefan931025-sys/cross-asset-momentum-carry.git
cd cross-asset-momentum-carry
python multi_factor_alpha.py
