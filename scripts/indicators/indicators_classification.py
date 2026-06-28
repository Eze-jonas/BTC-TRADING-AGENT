def classify_momentum(momentum: float):

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


def classify_rsi(rsi: float):

    if rsi < 30:
        return "OVERSOLD"

    elif rsi > 70:
        return "OVERBOUGHT"

    return "NEUTRAL"