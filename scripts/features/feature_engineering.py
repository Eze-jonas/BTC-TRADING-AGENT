import pandas as pd

def add_momentum(df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """
    Creates momentum feature from live_state["df"]
    """
    momentum_df = df.copy()

    momentum_df["momentum"] = momentum_df["close"].pct_change(window) * 100

    return momentum_df


def add_sma(momentum_df: pd.DataFrame, window: int = 10) -> pd.DataFrame:

    sma_df = momentum_df.copy()

    sma_df["sma"] = sma_df["close"].rolling(window=window).mean()
    sma_df["sma_pct"] = (sma_df["close"] - sma_df["sma"]) / sma_df["sma"] * 100

    return sma_df.dropna()

