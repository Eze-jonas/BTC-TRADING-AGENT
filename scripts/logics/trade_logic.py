
# BUY LOGIC
def buy(live_state, price, amount, reason="SIGNAL"):

    if amount > live_state["cash"]:
        amount = live_state["cash"]

    if amount <= 0:
        return

    qty = amount / price

    live_state["cash"] -= amount
    live_state["btc_holdings"] += qty
    live_state["current_price"] = price

    # =========================
    # AVERAGE ENTRY PRICE (DCA FIX)
    # =========================
    old_qty = live_state["btc_holdings"] - qty
    old_avg = live_state.get("avg_entry_price", 0.0)

    if old_qty == 0:
        avg_price = price
    else:
        avg_price = (
            (old_qty * old_avg) + (qty * price)
        ) / (old_qty + qty)

    live_state["avg_entry_price"] = avg_price

    # =========================
    # LABEL BUY VS DCA
    # =========================
    trade_type = "BUY"

    live_state["is_in_position"] = True

    live_state["trades"].append({
        "type": trade_type,
        "reason": reason,
        "strategy": live_state.get("selected_strategy", "UNKNOWN"),
        "price": price,
        "amount": amount,
        "qty": qty,
        "pnl": 0.0,
        "rsi": live_state.get("rsi"),
        "index": live_state["candle_count"]
    })

    print(f"{trade_type} EXECUTED @ {price}")


# SELL LOGIC
def sell(live_state, price, exit_reason="SIGNAL"):

    qty = live_state["btc_holdings"]

    if qty <= 0:
        return

    proceeds = qty * price

    entry_price = live_state.get("avg_entry_price", price)
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
        "reason": exit_reason,
        "strategy": live_state.get("selected_strategy", "UNKNOWN"),
        "price": price,
        "qty": qty,
        "proceeds": proceeds,
        "pnl": pnl,
        "rsi": live_state.get("rsi"),
        "index": live_state["candle_count"]
    })

    print(f"SELL EXECUTED @ {price}")

    # reset position state
    live_state["avg_entry_price"] = 0.0
    live_state["is_in_position"] = False