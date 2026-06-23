from scripts.states.live_state import live_state
from scripts.logics.trade_logic import buy, sell
from scripts.indicators.indicators_classification import classify_momentum
from scripts.configurations.parameter_configuration import config


def trade_strategy(candle):

    price = candle["close"]

    latest_df = live_state["df"]

    momentum = latest_df["momentum"].iloc[-1]

    regime = classify_momentum(momentum)

    live_state["momentum_regime"] = regime

    print(
        f"PRICE={price} | "
        f"MOMENTUM={momentum:.4f} | "
        f"REGIME={regime}"
    )

    is_long = live_state.get("btc_holdings", 0) > 0

    # =========================
    # ENTRY
    # =========================
    if regime == "BULLISH" and not is_long:

        buy(
            live_state,
            price,
            config["position_size"]
        )

    # =========================
    # EXIT
    # =========================
    elif regime == "BEARISH" and is_long:

        sell(live_state, price)