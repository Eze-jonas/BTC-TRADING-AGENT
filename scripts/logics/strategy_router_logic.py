def strategy_router(regime: str) -> str:

    if regime == "TRENDING":
        return "DAY"

    elif regime == "RANGING":
        return "SWING"

    elif regime == "DOWNTREND":
        return "SWING"

    return "SWING"