# BUY LOGIC
def buy(live_state, price, amount):

    if amount > live_state["cash"]:
        amount = live_state["cash"]

    if amount <= 0:
        return

    qty = amount / price

    live_state["cash"] -= amount
    live_state["btc_holdings"] += qty
    live_state["current_price"] = price

    # set entry price ALWAYS on buy
    live_state["entry_price"] = price

    live_state["trades"].append({
    "type": "BUY",
    "price": price,
    "amount": amount,
    "qty": qty,
    "pnl": 0.0,
    "index": live_state["candle_count"]
})

    print(f"BUY EXECUTED @ {price}")


# SELL LOGIC
def sell(live_state, price):

    qty = live_state["btc_holdings"]

    if qty <= 0:
        return

    proceeds = qty * price

    entry_price = live_state.get("entry_price", price)
    pnl = (price - entry_price) * qty

    live_state["cash"] += proceeds
    live_state["btc_holdings"] = 0
    live_state["current_price"] = price

    # =========================
    # UPDATE WIN / LOSS COUNTS
    # =========================
    if pnl > 0:
        live_state["wins"] += 1
    else:
        live_state["losses"] += 1

    live_state["trades"].append({
    "type": "SELL",
    "price": price,
    "qty": qty,
    "proceeds": proceeds,
    "pnl": pnl,
    "index": live_state["candle_count"]
})

    print(f"SELL EXECUTED @ {price}")

    # reset position state
    live_state["entry_price"] = 0.0