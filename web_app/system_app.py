from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio

from data.histo_data_loader import load_initial_data
from scripts.engine.live_runner import run_engine
from scripts.states.live_state import live_state
from scripts.engine.engine_controller import (
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

    df = load_initial_data()

    start_live_system()

    task = asyncio.create_task(run_engine(df))

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

                # ✅ ADD THIS FOR TABLE
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
                "sharpe_ratio": live_state.get("sharpe_ratio", 0),
                "max_dd": live_state.get("max_dd", 0),
                "equity_curve": live_state.get("equity_curve", [])[-500:],
                "profits": live_state.get("profits", 0),
            })

            await asyncio.sleep(1)

    except Exception:
        pass

# uvicorn web_app.system_app:app --reload --port 9000