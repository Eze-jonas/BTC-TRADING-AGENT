from scripts.indicators.indicators_classification import (
    classify_momentum,
    classify_sma_pct
)

from scripts.states.live_state import live_state


def build_state_summary(latest_row):
    return {
        "momentum": classify_momentum(latest_row["momentum"]),
        "sma": classify_sma_pct(latest_row["sma_pct"]),
        "rsi": latest_row["rsi"],
        "atr": latest_row["atr"],
    }


def build_market_summary(candle, state_summary, regime):
    return {
        "price": candle["close"],
        "momentum": state_summary["momentum"],
        "sma": state_summary["sma"],
        "rsi": state_summary["rsi"],
        "atr": state_summary["atr"],
        "regime": regime,
        "position": "LONG" if live_state.get("btc_holdings", 0) > 0 else "FLAT",
        "cash": live_state.get("cash", 10000),
        "btc": live_state.get("btc_holdings", 0),
    }
    