def classify_momentum(momentum):

    if momentum > 0:
        return "BULLISH"

    elif momentum < 0:
        return "BEARISH"

    return "NEUTRAL"