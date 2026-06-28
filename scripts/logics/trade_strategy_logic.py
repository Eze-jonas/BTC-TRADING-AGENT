from scripts.states.live_state import live_state
from scripts.logics.trade_logic import buy, sell
from scripts.logics.dca_logic import should_dca

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

    # =========================
    # ATR (NEW ADDITION)
    # =========================
    atr = latest_df["atr"].iloc[-1]

    momentum_regime = classify_momentum(momentum)
    sma_regime = classify_sma_pct(sma_pct)

    live_state["momentum_regime"] = momentum_regime
    live_state["sma_regime"] = sma_regime
    live_state["atr"] = atr

    print(
        f"PRICE={price} | "
        f"MOMENTUM={momentum:.4f} | "
        f"SMA_PCT={sma_pct:.4f} | "
        f"ATR={atr:.4f} | "
        f"MOMENTUM_REGIME={momentum_regime} | "
        f"SMA_REGIME={sma_regime}"
    )

    is_long = live_state.get("btc_holdings", 0) > 0

    # =========================
    # EXIT (HIGHEST PRIORITY)
    # =========================
    if momentum_regime == "BEARISH" and sma_regime == "BEARISH" and is_long:

        sell(
            live_state,
            price,
            exit_reason="SIGNAL"
        )
        return

    # =========================
    # ATR TRAILING STOP LOSS
    # =========================
    if is_long:

        entry_price = live_state.get("avg_entry_price", price)

        # initialize or update highest price
        highest_price = live_state.get(
            "highest_price_since_entry",
            entry_price
        )

        if price > highest_price:
            highest_price = price
            live_state["highest_price_since_entry"] = highest_price

        # trailing stop calculation
        stop_loss = highest_price - (
            atr * config["atr_multiplier"]
        )

        if price <= stop_loss:
            print(f"TRAILING ATR STOP HIT @ {price}")

            sell(
                live_state,
                price,
                exit_reason="ATR STOP"
            )
            return

    # =========================
    # ENTRY (FIRST BUY ONLY)
    # =========================
    if (
        momentum_regime == "BULLISH"
        and sma_regime == "BULLISH"
        and not is_long
    ):

        buy(
            live_state,
            price,
            config["position_size"],
            reason="SIGNAL"
        )

    # =========================
    # DCA (ACCUMULATION LAYER)
    # =========================
    if is_long:

        avg_entry_price = live_state["avg_entry_price"]

        if should_dca(
            price,
            avg_entry_price,
            config["dca_drop_pct"]
        ):

            buy(
                live_state,
                price,
                config["position_size"],
                reason="DCA"
            )

            print(
                f"DCA DEBUG | "
                f"PRICE={price} | "
                f"LAST_DCA_PRICE={live_state['last_dca_price']}"
            )

            print(
                f"DCA CHECK | "
                f"PRICE={price} | "
                f"AVG_ENTRY={live_state['avg_entry_price']}"
            )