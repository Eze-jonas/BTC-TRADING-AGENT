import pandas as pd
import logging

from data.binance_data_fetcher import fetch_klines

from scripts.configurations.parameter_configuration import config

logger = logging.getLogger(__name__)


def load_and_process_historical_data(
    symbol=config["symbol"],
    interval=config["interval"],
    lookback=config["lookback"]
):
    """"
    loads and processes binance historical raw data returned by fetch_klines()
    """  

    try:
        logger.info("Loading historical data from Binance...")

        raw = fetch_klines(symbol, interval, lookback)

        if not raw:
            raise ValueError("No historical data returned from Binance")

        h_df = pd.DataFrame(
            raw,
            columns=[
                "open_time", "open", "high", "low",
                "close", "volume",
                "close_time", "quote_asset_volume",
                "num_trades", "taker_buy_base",
                "taker_buy_quote", "ignore"
            ]
        )

        # keep only useful columns
        h_df = h_df[["open_time", "open", "high", "low", "close", "volume"]]

        # convert types
        h_df["open_time"] = pd.to_datetime(h_df["open_time"], unit="ms")

        h_df = h_df.set_index("open_time").sort_index()
        h_df = h_df.astype(float)

        logger.info(f"Historical dataset ready: {h_df.shape}")

        return h_df

    except Exception as e:
        logger.exception("Failed to load historical data")
        raise