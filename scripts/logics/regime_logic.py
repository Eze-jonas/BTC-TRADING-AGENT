def detect_regime(state):

    if state["momentum"] == "BULLISH" and state["sma"] == "BULLISH":
        return "TRENDING"

    elif state["momentum"] == "BEARISH" and state["sma"] == "BEARISH":
        return "DOWNTREND"

    else:
        return "RANGING"