# BTC Trading Agent/Bot

## Overview

This project presents the design and implementation of an intelligent **Bitcoin (BTC) Trading Agent/Bot** capable of operating on both historical and live market data obtained from Binance. The project explores the evolution of an algorithmic trading system from a simple rule-based strategy to a multi-strategy architecture incorporating market regime detection, dynamic strategy routing, and a Large Language Model (LLM)-based decision engine.

The system integrates historical backtesting, live market streaming, portfolio management, risk management, and an interactive web dashboard to provide a complete end-to-end cryptocurrency trading environment.

---

# Data Source

- **Exchange:** Binance
- **Asset:** BTCUSDT
- **Historical Data:** 2 Days
- **Timeframe:** 1 Minute Candlesticks

The following market variables were extracted from Binance historical kline data:

- Open Time
- Open Price
- High Price
- Low Price
- Close Price
- Trading Volume

---

# Data Pre-processing

The raw Binance dataset was converted into a Pandas DataFrame before further analysis.

The following preprocessing steps were performed:

- Converted **Open Time** into Python datetime format.
- Set **Open Time** as the DataFrame index.
- Converted:
  - Open
  - High
  - Low
  - Close
  - Volume

  into floating-point numerical values.

The processed dataset became the foundation for feature engineering, strategy development, backtesting, and live trading.

---

# Phase 1: Rule-Based Trading Agent

The first phase focused on developing a deterministic rule-based Bitcoin trading system.

A simple momentum strategy was implemented for market entry and exit.

## Trading Rules

### Buy Condition

- Momentum > 0

### Sell Condition

- Momentum < 0

---

## Dollar Cost Averaging (DCA)

A Dollar Cost Averaging (DCA) mechanism was implemented to increase Bitcoin holdings during favourable market conditions.

Additional BTC purchases were executed whenever the current market price declined by **3%** below the previous entry price.

This approach reduced the average acquisition cost while maintaining exposure during market pullbacks.

---

## ATR Trailing Stop Loss

Risk management was implemented using an **Average True Range (ATR)** trailing stop-loss.

Configuration:

- ATR Multiplier: **1.5**

The stop-loss dynamically adjusted according to market volatility, allowing profitable trades to continue while protecting accumulated gains.

---

## Feature Engineering

The following indicators were computed and added to the dataset:

- Momentum
- Average True Range (ATR)

These indicators formed the basis of the initial trading strategy.

---

## Portfolio Management

A portfolio manager was developed to simulate realistic trading.

The portfolio maintained:

- Cash balance
- BTC holdings
- Portfolio value
- Executed trades
- Trade history
- Portfolio statistics

The complete trading system was evaluated using historical replay (backtesting).

---

# Phase 2: Live Trading System

Following successful backtesting, the trading engine was integrated with Binance live streaming market data.

Incoming market data was continuously received, processed, and passed through the trading pipeline in real time.

The system was deployed using **FastAPI**, allowing the trading engine to run as a live web application.

---

# Interactive Dashboard

> **Insert dashboard screenshot below**

```md
![Live Dashboard](images/live_dashboard.png)
```

The dashboard was developed using:

- HTML
- Bootstrap
- JavaScript
- FastAPI

Users can interact with the trading bot through:

- Start Button
- Stop Button

A runtime counter continuously displays how long the trading bot has been running.

---

# Dashboard Components

## 1. Debug Section

Provides visibility into the internal state of the trading engine.

Displays:

- Indicator values
- Indicator status
- Trading signal status
- Internal debugging information

---

## 2. Portfolio & Performance Metrics

The dashboard displays live portfolio statistics including:

- Initial Capital
- Cash Balance
- BTC Holdings
- Current BTC Price
- Portfolio Value
- Number of Processed Candles
- Number of Trades
- Winning Trades
- Losing Trades
- Total Profit
- Sharpe Ratio
- Maximum Drawdown

---

## 3. Transaction History

Every executed trade is recorded within the transaction table.

Each transaction includes:

- Trade Type (Buy/Sell)
- Entry Price
- BTC Quantity
- Profit/Loss
- Candle Index
- Selected Strategy
  - Day Trade
  - Swing Trade
- Trade Reason

Example reasons include:

- Momentum Signal
- ATR Stop Loss
- RSI Take Profit
- DCA Entry

---

## 4. Portfolio Health Monitoring

A portfolio health monitoring module was implemented to reduce catastrophic losses.

The dashboard continuously calculates the current portfolio value as a percentage of the initial capital.

If the portfolio value falls below **25%** of its initial value:

- Trading automatically stops.
- Existing trading activity is terminated.

This safeguard protects the portfolio from excessive capital loss.

---

# Performance Visualisations

The dashboard also includes:

## Equity Curve

Displays portfolio growth throughout trading.

---

## Win/Loss Distribution

A pie chart visualises:

- Winning Trades
- Losing Trades

allowing quick assessment of trading performance.

---

# Phase 3: Strategy Improvement

To improve decision quality, additional technical indicators were introduced incrementally.

Each indicator produced a separate version of the trading system for evaluation.

Project versions included:

- Momentum
- Momentum + SMA
- Momentum + SMA + RSI

This incremental approach enabled individual assessment of each added indicator.

---

# Market Regime Detection

A market regime classification module was developed.

The market is classified into three regimes.

## Trending

Conditions:

- Bullish Momentum
- Bullish SMA

---

## Downtrending

Conditions:

- Bearish Momentum
- Bearish SMA

---

## Ranging

Any market conditions that are neither trending nor downtrending are classified as ranging.

---

# Trading Strategies

## Day Trading Strategy

### Entry Conditions

- Bullish Momentum
- Dollar Cost Averaging (DCA)

### Exit Conditions

- Bearish Momentum
- ATR Trailing Stop Loss

---

## Swing Trading Strategy

### Entry Conditions

- Bullish Momentum
- Bullish SMA
- RSI Buy Threshold
- Dollar Cost Averaging (DCA)

### Exit Conditions

- Bearish Momentum
- Bearish SMA
- ATR Trailing Stop Loss
- RSI Take Profit

Each strategy was independently evaluated and monitored before integration.

---

# Strategy Router

After validating both trading strategies independently, a strategy router was developed.

The router automatically selected the most appropriate trading strategy based on the detected market regime.

Routing logic:

| Market Regime | Selected Strategy |
|---------------|-------------------|
| Trending | Day Trading |
| Downtrending | Swing Trading |
| Ranging | Swing Trading |

The combined rule-based trading system dynamically switched between strategies according to prevailing market conditions.

---

# LLM-Based Strategy Router

The final phase investigated the use of a **Large Language Model (LLM)** for trading strategy selection.

The rule-based router was replaced with an **Ollama-hosted Llama 3.1** model.

Rather than relying on manually defined routing logic, the LLM analysed the current market context and selected the most appropriate trading strategy.

The LLM classified market conditions into:

- Day Trading
- Swing Trading

based on the available market indicators and trading context.

This enabled comparison between traditional deterministic routing and AI-driven strategy selection.

---

# System Architecture

The completed trading system consists of:

- Binance Historical Data
- Binance Live Streaming Data
- Data Pre-processing
- Feature Engineering
- Momentum Strategy
- SMA Strategy
- RSI Strategy
- Dollar Cost Averaging (DCA)
- ATR Trailing Stop Loss
- Portfolio Management
- Market Regime Detection
- Rule-Based Strategy Router
- LLM-Based Strategy Router (Llama 3.1)
- FastAPI Backend
- Interactive Dashboard
- Performance Analytics
- Backtesting Engine
- Live Trading Engine

---

# Technologies Used

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Data Processing | Pandas |
| Data Source | Binance API |
| Backend | FastAPI |
| Frontend | HTML |
| Styling | Bootstrap |
| Client Interaction | JavaScript |
| Charts | Chart.js |
| LLM | Ollama (Llama 3.1) |
| Version Control | Git |
| Streaming | Binance WebSocket |

---

# Conclusion

This project successfully demonstrates the complete development lifecycle of an intelligent Bitcoin trading system, beginning with a simple momentum-based rule engine and progressing toward a multi-strategy architecture capable of operating on live market data. Historical Binance data was used to develop, evaluate, and refine the trading logic before deploying the system in a real-time streaming environment with an interactive FastAPI dashboard.

Several risk management techniques were incorporated, including Dollar Cost Averaging (DCA), ATR-based trailing stop-loss, and automated portfolio health monitoring, enabling the trading agent to manage exposure while protecting capital. Performance was continuously monitored through portfolio metrics, transaction history, equity curve visualisation, and win/loss analysis.

To improve trading performance, additional technical indicators such as SMA and RSI were progressively introduced, leading to the development of specialised Day Trading and Swing Trading strategies. A market regime detection module and strategy router enabled automatic selection of the most suitable strategy based on prevailing market conditions.

Finally, the project explored the application of artificial intelligence by replacing the deterministic strategy router with an Ollama-hosted Llama 3.1 Large Language Model. This demonstrated how LLMs can be integrated into algorithmic trading systems to perform higher-level reasoning and strategy selection using structured market context.

Overall, the project provides a modular and extensible framework that combines traditional quantitative trading techniques with modern AI-driven decision making. The architecture is well suited for future enhancements such as additional technical indicators, alternative trading strategies, reinforcement learning, autonomous agent frameworks, improved risk management techniques, and support for multiple financial markets.