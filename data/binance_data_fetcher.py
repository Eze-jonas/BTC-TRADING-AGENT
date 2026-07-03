import time
import logging
from binance.client import Client

logger = logging.getLogger(__name__)

client = Client()


def fetch_klines(symbol, interval, lookback):
    """
    Fetch raw kline data from Binance with retry logic.
    """

    for attempt in range(3):
        try:
            logger.info(f"Fetching Binance data (attempt {attempt + 1}/3)...")

            return client.get_historical_klines(
                symbol,
                interval,
                lookback
            )

        except Exception as e:
            logger.warning(f"Binance fetch failed (attempt {attempt + 1}): {e}")
            time.sleep(2)

    raise Exception("Failed to fetch historical data after 3 retries")