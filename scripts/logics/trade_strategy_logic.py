from scripts.states.live_state import live_state
from scripts.logics.trade_logic import buy, sell


def trade_strategy(candle):

    price = candle["close"]
    print(f"PROCESSING: {price}")

    previous_close = live_state.get("previous_close")

    # initialize first time
    if previous_close is None:
        live_state["previous_close"] = price
        return

    drop = (previous_close - price) / previous_close * 100
    rise = (price - previous_close) / previous_close * 100

    is_long = live_state.get("btc_holdings", 0) > 0

    # BUY (only if NOT already in position)
    if drop >= 0.005 and not is_long:

        buy(live_state, price, 1000)

    # SELL (only if in position)
    elif rise >= 0.005 and is_long:

        sell(live_state, price)

    # UPDATE PREVIOUS CLOSE
    live_state["previous_close"] = price