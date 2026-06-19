from data.histo_data_loader import load_initial_data

from scripts.states.live_state import live_state
from scripts.values.portfolio_value import portfolio_value

from scripts.engine.process_candle import process_candle


# =========================
# 1. LOAD DATASET
# =========================
df = load_initial_data()


# =========================
# 2. INIT PORTFOLIO STATE
# =========================
live_state["current_price"] = df.iloc[0]["close"]


# =========================
# 3. RUN BACKTEST LOOP
# =========================
for _, candle in df.iterrows():

    # send each candle into engine
    process_candle(candle)

    # OPTIONAL: live valuation print
    value = portfolio_value(live_state)
    print(f"Portfolio Value: {value}")


# =========================
# 4. FINAL OUTPUT
# =========================
print("\nFINAL PORTFOLIO:")
print(live_state)

print("\nFINAL VALUE:")
print(portfolio_value(live_state))