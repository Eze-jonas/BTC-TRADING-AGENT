import asyncio

from scripts.states.live_state import live_state
from scripts.engine.process_candle import process_candle

from scripts.analytics.metrics import (
    update_portfolio_value,
    update_equity_curve,
    update_sharpe,
    update_max_dd,
    update_profits
)

running = False


async def run_engine(df):

    global running
    running = True

    print("ENGINE STARTED")
    

    for _, candle in df.iterrows():

        if not running:
            print("ENGINE STOPPED")
            break

        # =========================
        # PHASE 1: PROCESS CANDLE
        # =========================
        process_candle(candle)

        live_state["candle_count"] += 1

        # =========================
        # PHASE 2: METRICS (AFTER FULL PROCESSING)
        # =========================
        update_portfolio_value()
        update_equity_curve()
        update_sharpe()
        update_max_dd()
        update_profits() 
        print("PORTFOLIO:", live_state.get("portfolio_value"))
        print("WINS:", live_state.get("wins"))

        await asyncio.sleep(1)

    print("ENGINE FINISHED")


def stop_engine():

    global running
    running = False