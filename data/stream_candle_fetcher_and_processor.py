import json
import websockets
import pandas as pd

WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


async def fetch_and_process_stream_candle():
    """
    fetches and processes binance live streaming data and produces candle
    """

    async with websockets.connect(WS_URL) as ws:

        while True:

            msg = await ws.recv()
            data = json.loads(msg)

            k = data["k"]

            # ONLY process CLOSED candles
            if not k["x"]:
                continue

            candle = {
                "open_time": pd.to_datetime(k["t"], unit="ms"),
                "open": float(k["o"]),
                "high": float(k["h"]),
                "low": float(k["l"]),
                "close": float(k["c"]),
                "volume": float(k["v"])
            }

            yield candle