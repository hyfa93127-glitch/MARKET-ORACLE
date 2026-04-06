# Stock Predictor Technical Documentation

This document provides a detailed overview of the Stock Predictor platform, its architecture, and its core analytical features.

---

## 1. Project Overview

The **Stock Predictor** is an end-to-end Machine Learning system designed to analyze market trends and suggest optimized investment allocations. It uses **Classification-based Random Forest models** to predict whether a stock's price will move **UP** or **DOWN** on the next trading day.

---

## 2. System Architecture

The project follows a modular, layer-based architecture:

1.  **Data Ingestion (`src/ingestion.py`)**: Fetches historical market data (Open, High, Low, Close, Volume) from the Yahoo Finance API using `yfinance`.
2.  **Feature Engineering (`src/features.py`)**: Transforms raw data into a technical indicator suite, including:
    -   **RSI (Relative Strength Index)**: Momentum indicator for overbought/oversold conditions.
    -   **MACD (Moving Average Convergence Divergence)**: Trend-following momentum.
    -   **Bollinger Bands**: Volatility and price level analysis.
    -   **Moving Averages (10/20 day)**: Simple trend smoothing.
3.  **ML Pipeline (`src/train.py` & `src/predict.py`)**:
    -   **Training**: Trains a specialized Random Forest model for EACH ticker. It learns patterns from historical features to predict future price direction.
    -   **Prediction**: Generates both a binary outcome ("UP" or "DOWN") and a **Confidence Score** (probability).
4.  **Portfolio Allocator (`src/allocator.py`)**: Analyzes multiple predictions and suggests a budget distribution.
5.  **User Interfaces**: 
    -   **Streamlit Dashboard**: A visual interface for interactive analysis.
    -   **FastAPI Backend**: A programmatic interface for integration with other apps.

---

## 3. Core Analytical Features

### 📅 Advanced Dashboard Navigation
- **Date Range Filter**: Allows users to zoom into specific historical periods (e.g., 2024 vs 2026).
- **Upcoming Events Tab**: Integrates live corporate calendars (Earnings and Dividends) directly from `yfinance`.

### 💰 Smart Portfolio Allocator
The allocator helps users maximize returns by intelligently splitting their capital.
- **Algorithm**: Confident-Weighted Allocation.
- **Rules**:
    1.  Only tickers predicted "UP" with >50% confidence are considered.
    2.  Budget is split proportionally—stocks with higher model confidence receive a larger share of the budget.
    3.  Calculates exact share counts and cost per ticker, accounting for current prices.

---

## 4. Pipeline Orchestration

The system is controlled via `pipeline.py`, which ensures data consistency:
1.  Downloads latest prices.
2.  Updates technical indicators for the new data.
3.  Retrains models if necessary.
4.  Evaluates performance (Accuracy, F1-Score).

---

## 5. Handling Market Holidays

The system is designed to handle gaps in trading data (e.g., weekends or Good Friday). 
- **Inference Logic**: The model always uses the *latest available* trading data to predict the *next future* trading day, ensuring that predictions remain relevant even after holiday closures.

---

## 6. How to Extend the Project

### Adding New Tickers
1.  Open `config.yaml`.
2.  Add the new symbol (e.g., `NFLX`, `BTC-USD`) to the `tickers` list.
3.  Run `python pipeline.py` to train a new model for that ticker.

### Modifying Hyperparameters
Model complexity (e.g., number of trees) can be tuned in the `model` section of `config.yaml`:
```yaml
model:
  n_estimators: 100
  random_state: 42
```

---

## 7. API Reference

The FastAPI backend provides a `/predict/{ticker}` endpoint:
- **Input**: Ticker Symbol (e.g., AAPL).
- **Output**: JSON payload with the predicted direction.
- **Docs**: Available at `http://localhost:8000/docs`.
