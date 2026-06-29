import pandas as pd

# ADD MOMENTUM
def add_momentum(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Creates momentum feature from live_state["df"]
    """
    momentum_df = df.copy()

    momentum_df["momentum"] = momentum_df["close"].pct_change(window) * 100

    return momentum_df

# ADD SMA
def add_sma(momentum_df: pd.DataFrame, window: int) -> pd.DataFrame:

    sma_df = momentum_df.copy()

    sma_df["sma"] = sma_df["close"].rolling(window=window).mean()
    sma_df["sma_pct"] = (sma_df["close"] - sma_df["sma"]) / sma_df["sma"] * 100

    return sma_df

# ADD ATR
def add_atr(sma_df: pd.DataFrame, window: int):

    atr_df = sma_df.copy()

    high = atr_df["high"]
    low = atr_df["low"]
    close = atr_df["close"]

    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr_df["atr"] = true_range.rolling(window=window).mean()

    return atr_df
# ADD RSI
import pandas as pd

def add_rsi(atr_df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Adds Relative Strength Index (RSI) feature.
    """

    rsi_df = atr_df.copy()

    delta = rsi_df["close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss

    rsi_df["rsi"] = 100 - (100 / (1 + rs))

    return rsi_df