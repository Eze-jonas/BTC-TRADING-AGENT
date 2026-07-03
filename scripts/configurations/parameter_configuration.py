from binance.client import Client

config = {
    "position_size": 1000,
    "portfolio_stop_pct": 0.25,
    "dca_drop_pct": 0.0002,

    # Historical data
    "symbol": "BTCUSDT",
    "interval": Client.KLINE_INTERVAL_1MINUTE,
    "lookback": "2 days ago UTC",

    # Indicators
    "momentum_window": 10,
    "sma_window": 10,
    "rsi_window": 10,
    "atr_window": 14,
    "atr_multiplier": 1.5,

    # RSI thresholds (SWING LOGIC)
    "rsi_buy_threshold": 65,
    "rsi_sell_threshold": 70,
    
     # LLM
    "llm_model": "llama3.1",
    "llm_temperature": 0,
}