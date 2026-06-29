from scripts.states.live_state import live_state
from scripts.logics.day_strategy_logic import day_strategy
from scripts.logics.swing_strategy_logic import swing_strategy


def trade_strategy(candle, latest_row):

    price = candle["close"]

    strategy = live_state.get("selected_strategy", "DAY")
    print("SELECTED STRATEGY =", strategy)
    if strategy == "DAY":
        day_strategy(price, latest_row)

    elif strategy == "SWING":
        swing_strategy(price, latest_row)

  