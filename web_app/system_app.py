from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio

from data.historical_data_loader_and_processor import (
    load_and_process_historical_data
)
from data.stream_candle_fetcher_and_processor import fetch_and_process_stream_candle
from data.feature_engineering import add_momentum
from scripts.logics.logics_runner import logics_runner
from scripts.states.live_state import live_state
from scripts.controllers.bot_controller import (
    start_live_system,
    stop_live_system
)

from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="web_app/static"), name="static")

task = None


# =========================
# DASHBOARD PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
async def dashboard():

    with open("web_app/templates/dashboard.html", "r") as f:
        return f.read()


# =========================
# START SYSTEM
# =========================
@app.post("/start")
async def start():

    global task

    # =========================
    # LOAD + PROCESS HISTORICAL DATA
    # =========================
    h_df = load_and_process_historical_data()

    # FEATURE ENGINEERING (ADD THIS)
    df = add_momentum(h_df)

    print("HDF SHAPE:", df.shape)
    print(df.tail())

    # =========================
    # ATTACH TO LIVE STATE
    # =========================
    live_state["df"] = df

    start_live_system()

    # =========================
    # START STREAMING LOGICS
    # =========================
    task = asyncio.create_task(
        logics_runner(fetch_and_process_stream_candle)
    )

    return {"status": "started"}


# =========================
# STOP SYSTEM
# =========================
@app.post("/stop")
def stop():

    global task

    stop_live_system()

    if task:
        task.cancel()
        task = None

    return {"status": "stopped"}


# =========================
# LIVE WEBSOCKET STREAM
# =========================
@app.websocket("/ws")
async def ws(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:

            runtime_seconds = 0

            if live_state.get("start_time"):
                runtime_seconds = (
                    datetime.utcnow() - live_state["start_time"]
                ).total_seconds()

            await websocket.send_json({
                # =========================
                # CORE STATE
                # =========================
                "status": live_state.get("status", "STOPPED"),
                "price": live_state.get("current_price", 0),
                "cash": live_state.get("cash", 0),
                "btc_holdings": live_state.get("btc_holdings", 0),

                "trades_count": live_state.get("wins", 0)
                    + live_state.get("losses", 0),

                "last_trade": live_state.get("trades", [])[-1]
                    if live_state.get("trades") else None,

                # =========================
                # TRADES TABLE
                # =========================
                "trades": live_state.get("trades", []),

                "candle_count": live_state.get("candle_count", 0),

                # =========================
                # RUNTIME
                # =========================
                "runtime_seconds": runtime_seconds,

                # =========================
                # METRICS
                # =========================
                "portfolio_value": live_state.get("portfolio_value", 0),
                "wins": live_state.get("wins", 0),
                "losses": live_state.get("losses", 0),
                "win_rate": live_state.get("win_rate", 0),
                "sharpe_ratio": live_state.get("sharpe_ratio", 0),
                "max_dd": live_state.get("max_dd", 0),
                "equity_curve": live_state.get("equity_curve", [])[-500:],
                "profits": live_state.get("profits", 0),

                # DEBUGS
                "momentum": live_state.get("momentum_regime", "NEUTRAL"),
            })

            await asyncio.sleep(1)

    except Exception:
        pass


# uvicorn web_app.system_app:app --reload --port 9000