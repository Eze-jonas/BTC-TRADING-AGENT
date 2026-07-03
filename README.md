# BTC Trading Agent/Bot

An intelligent Bitcoin (BTC) trading system that combines traditional algorithmic trading techniques with AI-driven strategy selection. The project evolved from a simple momentum-based trading bot into a modular trading framework supporting multiple strategies, market regime detection, live Binance streaming, portfolio management, and an LLM-powered strategy router using **Ollama Llama 3.1**.

---

## Overview

This project explores the development of an end-to-end cryptocurrency trading system capable of operating on both historical and live market data from Binance.

The trading engine was developed incrementally, beginning with a rule-based momentum strategy and progressively introducing additional technical indicators, multiple trading strategies, market regime detection, and AI-assisted strategy routing. The final system integrates real-time market streaming, portfolio management, automated risk management, and an interactive web dashboard for monitoring trading performance.

---

## Features

### Trading Engine

* Rule-based Bitcoin trading engine
* Historical replay (backtesting)
* Live trading using Binance WebSocket
* Modular strategy architecture
* Automatic strategy routing

### Trading Strategies

* Day Trading
* Swing Trading
* Market Regime Detection
* Rule-Based Strategy Router
* LLM-Based Strategy Router (Ollama Llama 3.1)

### Technical Indicators

* Momentum
* Simple Moving Average (SMA)
* Relative Strength Index (RSI)
* Average True Range (ATR)

### Risk Management

* Dollar Cost Averaging (DCA)
* ATR Trailing Stop Loss
* Portfolio Health Protection
* Portfolio Management

### Dashboard

* Real-time portfolio monitoring
* Live trade history
* Performance analytics
* Equity curve
* Win/Loss visualization
* Runtime monitoring
* Debug information

---

## Data Pipeline

Historical BTCUSDT candlestick data was collected from the Binance exchange using 1-minute intervals spanning two days.

The following market variables are extracted:

* Open Time
* Open
* High
* Low
* Close
* Volume

The preprocessing pipeline performs:

* Conversion of timestamps into Python datetime objects
* Datetime indexing
* Numerical conversion of market variables
* Feature engineering
* Technical indicator generation

The processed dataset is then used for backtesting, live trading, and performance evaluation.

---

## Trading Workflow

```text
Binance Historical Data
        │
        ▼
Data Pre-processing
        │
        ▼
Feature Engineering
(Momentum • SMA • RSI • ATR)
        │
        ▼
Market Regime Detection
        │
        ▼
Strategy Router
        │
   ┌────┴────┐
   ▼         ▼
Day Trade  Swing Trade
        │
        ▼
Portfolio Manager
        │
        ▼
Performance Analytics
        │
        ▼
FastAPI Dashboard
```

---

## Trading Strategies

### Day Trading

#### Entry

* Bullish Momentum
* Dollar Cost Averaging (DCA)

#### Exit

* Bearish Momentum
* ATR Trailing Stop Loss

---

### Swing Trading

#### Entry

* Bullish Momentum
* Bullish SMA
* RSI Buy Threshold
* Dollar Cost Averaging (DCA)

#### Exit

* Bearish Momentum
* Bearish SMA
* ATR Trailing Stop Loss
* RSI Take Profit

---

## Market Regime Detection

The market is automatically classified into three regimes:

| Market Regime | Conditions                        | Strategy      |
| ------------- | --------------------------------- | ------------- |
| Trending      | Bullish Momentum + Bullish SMA    | Day Trading   |
| Downtrending  | Bearish Momentum + Bearish SMA    | Swing Trading |
| Ranging       | Neither Trending nor Downtrending | Swing Trading |

This allows the trading engine to dynamically switch strategies according to current market conditions.

---

## LLM Strategy Router

The final stage of the project investigates the use of Large Language Models (LLMs) for trading strategy selection.

Instead of relying solely on manually defined routing rules, an **Ollama-hosted Llama 3.1** model analyses the current market context and determines whether the trading engine should execute the Day Trading or Swing Trading strategy.

This demonstrates how LLMs can be integrated into algorithmic trading systems to perform higher-level reasoning while preserving deterministic trade execution and risk management.

---

## Dashboard

The project includes an interactive dashboard built with FastAPI, HTML, Bootstrap, and JavaScript.

### Dashboard Screenshot

The dashboard provides:

### Portfolio Metrics

* Initial Capital
* Cash Balance
* BTC Holdings
* Current BTC Price
* Portfolio Value
* Profit
* Sharpe Ratio
* Maximum Drawdown

### Trading Statistics

* Processed Candles
* Executed Trades
* Winning Trades
* Losing Trades

### Transaction History

Each trade records:

* Buy/Sell
* Entry Price
* Quantity
* Profit/Loss
* Candle Index
* Selected Strategy
* Trade Reason

### Portfolio Health

The dashboard continuously monitors overall portfolio value.

If the portfolio falls below **25%** of its initial value, trading is automatically terminated to protect capital.

### Performance Visualizations

* Equity Curve
* Win/Loss Pie Chart

---

## Technology Stack

| Category             | Technology        |
| -------------------- | ----------------- |
| Programming Language | Python            |
| Data Processing      | Pandas            |
| Exchange API         | Binance API       |
| Live Streaming       | Binance WebSocket |
| Backend              | FastAPI           |
| Frontend             | HTML              |
| Styling              | Bootstrap         |
| Client Interaction   | JavaScript        |
| Charts               | Chart.js          |
| AI                   | Ollama            |
| LLM                  | Llama 3.1         |
| Version Control      | Git               |

---

## Project Structure

```text
btc_bot/
│
├── data/
├── images/
├── notebook/
├── scripts/
│   ├── analytics/
│   ├── configurations/
│   ├── engine/
│   ├── features/
│   ├── indicators/
│   ├── logics/
│   ├── sentiment/
│   ├── state/
│   ├── strategy/
│   └── ...
│
├── web_app/
│   ├── static/
│   ├── templates/
│   └── system_app.py
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/Eze-jonas/Wx3SQgsPYns0atJR.git
```

Navigate into the project.

```bash
cd btc_bot
```

Create and activate a virtual environment.

**Windows**

```bash
python -m venv BTC
BTC\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Install and start Ollama.

```bash
ollama pull llama3.1
ollama serve
```

---

## Running the Application

Start the FastAPI application.

```bash
uvicorn web_app.system_app:app --reload --port 9000
```

Open your browser.

```text
http://127.0.0.1:9000
```

Use the dashboard controls to start or stop the trading bot while monitoring portfolio performance in real time.

---

## Performance Evaluation

The project was evaluated through multiple development stages:

* Rule-based momentum trading
* Momentum + SMA
* Momentum + SMA + RSI
* Day Trading strategy
* Swing Trading strategy
* Rule-Based Strategy Router
* LLM-Based Strategy Router

Each stage was independently tested and monitored to evaluate the impact of additional indicators and strategy improvements on trading performance.

---

##  Future Improvements

Potential enhancements include:
* Additional technical indicators
* Reinforcement Learning
* Cloud deployment
* Telegram and email notifications
* Advanced portfolio optimisation

---

# Conclusion

This project successfully demonstrates the complete development lifecycle of an intelligent Bitcoin trading system, beginning with a simple momentum-based rule engine and progressing toward a multi-strategy architecture capable of operating on live market data. Historical Binance data was used to develop, evaluate, and refine the trading logic before deploying the system in a real-time streaming environment with an interactive FastAPI dashboard.

Several risk management techniques were incorporated, including Dollar Cost Averaging (DCA), ATR-based trailing stop-loss, and automated portfolio health monitoring, enabling the trading agent to manage exposure while protecting capital. Performance was continuously monitored through portfolio metrics, transaction history, equity curve visualisation, and win/loss analysis.

To improve trading performance, additional technical indicators such as SMA and RSI were progressively introduced, leading to the development of specialised Day Trading and Swing Trading strategies. A market regime detection module and strategy router enabled automatic selection of the most suitable strategy based on prevailing market conditions.

Finally, the project explored the application of artificial intelligence by replacing the deterministic strategy router with an Ollama-hosted Llama 3.1 Large Language Model. This demonstrated how LLMs can be integrated into algorithmic trading systems to perform higher-level reasoning and strategy selection using structured market context.

Overall, the project provides a modular and extensible framework that combines traditional quantitative trading techniques with modern AI-driven decision making. The architecture is well suited for future enhancements such as additional technical indicators, alternative trading strategies, reinforcement learning, autonomous agent frameworks, improved risk management techniques, and support for multiple financial markets.
