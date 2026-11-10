# Cross-Asset Momentum & Carry Alpha Engine

[![Cross-Asset Momentum CI](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/stefan931025-sys/cross-asset-momentum-carry)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A systematic multi-factor alpha generation engine combining time-series momentum, carry yield differentials, and target volatility position scaling across liquid asset classes.

---

## Strategy Design & Core Features

* **Multi-Factor Alpha Construction:** Combines normalized momentum $Z\text{-scores}$ (60% weight) and yield carry differentials (40% weight).
* **Volatility Targeting:** Dynamically scales leverage and position sizes based on rolling annualized asset volatility relative to portfolio target risk.
* **Risk Controls:** Enforces hard portfolio caps on leverage, asset concentration, and maximum drawdown parameters.

---

## Mathematical Specifications

### 1. Multi-Factor Alpha Score
$$\alpha_i = w_{\text{mom}} Z(\text{Momentum}_i) + w_{\text{carry}} Z(\text{Carry}_i)$$

### 2. Volatility-Targeted Position Sizing
$$w_i^* = \frac{\sigma_{\text{target}}}{\sigma_{i,t}} \cdot \tanh(\alpha_i)$$

---

## System Architecture & Data Flow

