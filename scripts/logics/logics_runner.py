import asyncio

from scripts.states.live_state import live_state

from scripts.logics.live_state_dataframe_updater import update_live_state_dataframe
from scripts.logics.trade_strategy_logic import trade_strategy

from scripts.logics.metrics_logic import (
    update_portfolio_value,
    update_equity_curve,
    update_sharpe,
    update_max_dd,
    update_profits,
    update_win_rate
)


running = False


# =========================
# LOGICS RUNNER (MAIN ORCHESTRATOR)
# =========================
async def logics_runner(stream_callback):

    global running
    running = True

    print("LOGICS RUNNER STARTED")

    async for candle in stream_callback():

        if not running:
            print("LOGICS RUNNER STOPPED")
            break

        # =========================
        # PHASE 1: DATA UPDATE
        # =========================
        update_live_state_dataframe(candle)

        # =========================
        # PHASE 2: STRATEGY EXECUTION
        # =========================
        trade_strategy(candle)

        # =========================
        # INCREMENT CANDLE COUNT
        # =========================
        live_state["candle_count"] += 1

        # =========================
        # PHASE 3: METRICS UPDATE
        # =========================
        update_portfolio_value()
        update_win_rate()
        update_equity_curve()
        update_sharpe()
        update_max_dd()
        update_profits()

        # =========================
        # DEBUG OUTPUT
        # =========================
        print("PORTFOLIO:", live_state.get("portfolio_value"))
        print("WINS:", live_state.get("wins"))

        await asyncio.sleep(0)  # keeps event loop responsive

    print("LOGICS RUNNER FINISHED")


# =========================
# STOP FUNCTION
# =========================
def stop_logics_runner():
    global running
    running = False