# Cross-Asset Momentum & Carry Alpha Engine

![CI Workflow](https://github.com/stefan931025-sys/cross-asset-momentum-carry/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A systematic multi-factor alpha generation engine combining time-series momentum, carry yield differentials, and target volatility position scaling across liquid asset classes[span_3](start_span)[span_3](end_span).

## 🚀 Strategy Design & Core Features

* **Multi-Factor Alpha Construction:** Combines normalized momentum Z-scores (60% weight) and yield differentials (40% weight)[span_4](start_span)[span_4](end_span).
* **Volatility Targeting:** Dynamically scales leverage and position sizes based on rolling annualized asset volatility relative to portfolio target risk[span_5](start_span)[span_5](end_span).
* **Risk Controls:** Enforces hard portfolio caps on leverage, asset concentration, and maximum drawdown parameters[span_6](start_span)[span_6](end_span).

---

## 📊 Mathematical Specifications

### 1. Multi-Factor Alpha Score

$$x_i = w_{\text{mom}} Z(\text{Momentum}) + w_{\text{carry}} Z(\text{Carry})$$

### 2. Volatility-Targeted Position Sizing

$$w_i^* = \frac{\sigma^{\text{Target}}}{\sigma_{c,i}} \cdot \tanh(x_i)$$

---

## 📁 Repository Structure

```text
cross-asset-momentum-carry/
├── .devcontainer/     # Devcontainer configuration for Codespaces
├── .github/
│   └── workflows/
│       └── ci.yml     # GitHub Actions automated test workflow
├── core/
│   └── macro_overlay.py # Multi-factor alpha & macro overlay modules
├── tests/
│   └── test_macro_overlay.py # Automated pytest suite
├── main.py            # Main execution pipeline script
├── repo_auditor.py    # Static AST analysis governance tool
├── requirements.txt   # Python dependencies
└── README.md          # System documentation
