from scripts.states.live_state import live_state
from scripts.executor.execution import buy, sell


def process_candle(candle):

    price = candle["close"]
    print(f"PROCESSING: {price}")

    last_price = live_state.get("last_price")

    # initialize first time
    if last_price is None:
        live_state["last_price"] = price
        return

    drop = (last_price - price) / last_price * 100
    rise = (price - last_price) / last_price * 100

    is_long = live_state.get("btc_holdings", 0) > 0

    # BUY (only if NOT already in position)
    if drop >= 0.05 and not is_long:

        buy(live_state, price, 1000)

    # SELL (only if in position)
    elif rise >= 0.05 and is_long:

        sell(live_state, price)

    # UPDATE PRICE TRACKER
    live_state["last_price"] = price