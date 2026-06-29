import asyncio
import pandas as pd

from scripts.states.live_state import live_state

from scripts.logics.live_state_dataframe_updater import update_live_state_dataframe
from scripts.logics.trade_strategy_logic import trade_strategy
from scripts.configurations.parameter_configuration import config
from scripts.logics.regime_logic import detect_regime
from scripts.logics.strategy_router_logic import strategy_router

from scripts.features.feature_engineering import (
    add_momentum,
    add_sma,
    add_atr,
    add_rsi
)

from scripts.indicators.indicators_classification import (
    classify_momentum,
    classify_sma_pct
)

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
        # STEP 1: CANDLE RECEIVED
        # =========================
        print("✅ CANDLE RECEIVED:", candle)

        # =========================
        # PHASE 1: UPDATE DATA
        # =========================
        update_live_state_dataframe(candle)
        live_state["current_price"] = candle["close"]
        print("✅ DF UPDATED")

        # DEBUG DF
        try:
            print("📊 DF SHAPE:", live_state["df"].shape)
            print(live_state["df"].tail(1))
        except Exception as e:
            print("❌ DF ERROR:", e)

        # =========================
        # FEATURE ENGINEERING
        # =========================
        try:
            df = live_state["df"]

            df = add_momentum(df, config["momentum_window"])
            df = add_sma(df, config["sma_window"])
            df = add_atr(df, config["atr_window"])
            df = add_rsi(df, config["rsi_window"])

            live_state["df"] = df

            print("✅ FEATURES DONE")

        except Exception as e:
            print("❌ FEATURE ENGINEERING FAILED:", e)
            continue

        # =========================
        # CLEAN DATASET
        # =========================
        clean_df = live_state["df"].dropna()

        if len(clean_df) == 0:
            print("⏳ WARMUP - waiting for indicators...")
            continue

        latest_row = clean_df.iloc[-1]

        # =========================
        # STEP 2: MARKET SUMMARY
        # =========================
        try:
            live_state["state_summary"] = {
                "momentum": classify_momentum(latest_row["momentum"]),
                "sma": classify_sma_pct(latest_row["sma_pct"]),
                "rsi": latest_row["rsi"],
                "atr": latest_row["atr"],
            }

            regime = detect_regime(live_state["state_summary"])
            live_state["regime"] = regime

            # AFTER MARKET SUMMARY (IMPORTANT FIX)
            live_state["rsi"] = latest_row["rsi"]
            live_state["atr"] = latest_row["atr"]
            live_state["momentum"] = classify_momentum(latest_row["momentum"])
            live_state["sma_pct"] = classify_sma_pct(latest_row["sma_pct"])

            live_state["selected_strategy"] = strategy_router(regime)

            print("STATE SUMMARY:", live_state["state_summary"])
            print("✅ MARKET SUMMARY DONE | REGIME:", regime)
            print("🚦 REGIME:", regime)
            print("🎯 ROUTED STRATEGY:", live_state["selected_strategy"])

        except Exception as e:
            print("❌ MARKET SUMMARY FAILED:", e)

        # =========================
        # PHASE 2: STRATEGY
        # =========================
        try:
            print("✅ ABOUT TO RUN STRATEGY")

            trade_strategy(candle, latest_row)

            print("✅ STRATEGY EXECUTED")

        except Exception as e:
            print("❌ STRATEGY FAILED:", e)

        # =========================
        # DEBUG DF (ALWAYS AFTER)
        # =========================
        print("ORIGINAL:", len(live_state["df"]))
        print("CLEAN:", len(clean_df))

        print("📊 CLEAN DF (HEAD)")
        print(clean_df.head(10))

        print("📊 CLEAN DF (TAIL)")
        print(clean_df.tail(3))

        # =========================
        # INCREMENT CANDLE COUNT
        # =========================
        live_state["candle_count"] += 1
        print("📈 CANDLE COUNT:", live_state["candle_count"])

        # =========================
        # PHASE 3: METRICS
        # =========================
        update_portfolio_value()
        update_win_rate()
        update_equity_curve()
        update_sharpe()
        update_max_dd()
        update_profits()

        print("💰 PORTFOLIO:", live_state.get("portfolio_value"))
        print("🏆 WINS:", live_state.get("wins"))

        await asyncio.sleep(0)

    print("LOGICS RUNNER FINISHED")


# =========================
# STOP FUNCTION
# =========================
def stop_logics_runner():
    global running
    running = False