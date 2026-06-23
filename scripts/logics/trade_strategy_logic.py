from scripts.states.live_state import live_state
from scripts.logics.trade_logic import buy, sell
from scripts.indicators.indicators_classification import (
    classify_momentum,
    classify_sma_pct
    )
from scripts.configurations.parameter_configuration import config


def trade_strategy(candle):

    price = candle["close"]

    latest_df = live_state["df"]

    momentum = latest_df["momentum"].iloc[-1]
    sma_pct = latest_df["sma_pct"].iloc[-1]

    momentum_regime = classify_momentum(momentum)
    sma_regime = classify_sma_pct(sma_pct)

    live_state["momentum_regime"] = momentum_regime
    live_state["sma_regime"] = sma_regime

    print(
        f"PRICE={price} | "
        f"MOMENTUM={momentum:.4f} | "
        f"SMA_PCT={sma_pct:.4f} | "
        f"MOMENTUM_REGIME={momentum_regime} | "
        f"SMA_REGIME={sma_regime}"
    )

    is_long = live_state.get("btc_holdings", 0) > 0

    # ENTRY
    if momentum_regime == "BULLISH" and sma_regime == "BULLISH" and not is_long:

        buy(live_state, price, config["position_size"])

    # EXIT
    elif momentum_regime == "BEARISH" and sma_regime == "BEARISH" and is_long:

        sell(live_state, price)