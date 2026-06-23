def classify_momentum(momentum):

    if momentum > 0:
        return "BULLISH"

    elif momentum < 0:
        return "BEARISH"

    return "NEUTRAL"

def classify_sma_pct(sma_pct: float):

    if sma_pct > 0:
        return "BULLISH"

    elif sma_pct < 0:
        return "BEARISH"

    return "NEUTRAL"