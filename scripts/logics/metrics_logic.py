import math
from scripts.states.live_state import live_state


# =========================
# PORTFOLIO VALUE
# =========================
def update_portfolio_value():

    price = live_state.get("current_price", 0)

    live_state["portfolio_value"] = (
        live_state.get("cash", 0)
        + live_state.get("btc_holdings", 0) * price
    )


# =========================
# EQUITY CURVE
# =========================
def update_equity_curve():

    if "portfolio_value" not in live_state:
        live_state["portfolio_value"] = 0

    live_state.setdefault("equity_curve", [])

    live_state["equity_curve"].append(
        live_state["portfolio_value"]
    )

    print("EQUITY POINTS:", len(live_state["equity_curve"]))


# =========================
# WIN / LOSS TRACKING
# =========================
def register_trade(trade):

    live_state.setdefault("trades", [])
    live_state["trades"].append(trade)

    live_state.setdefault("wins", 0)
    live_state.setdefault("losses", 0)

    pnl = trade.get("pnl", 0)

    live_state["wins"] += 1 if pnl > 0 else 0
    live_state["losses"] += 1 if pnl <= 0 else 0
    
# .................
# Lin/Loss Rate
#..................
def update_win_rate():
    wins = live_state.get("wins", 0)
    losses = live_state.get("losses", 0)

    total = wins + losses

    live_state["win_rate"] = wins / total if total > 0 else 0

# =========================
# SHARPE RATIO (simple version)
# =========================
def update_sharpe():

    curve = live_state.get("equity_curve", [])

    if len(curve) < 2:
        live_state["sharpe_ratio"] = 0
        return

    mean = sum(curve) / len(curve)

    variance = sum((x - mean) ** 2 for x in curve) / len(curve)
    std = math.sqrt(variance)

    live_state["sharpe_ratio"] = (mean / std) if std != 0 else 0


# =========================
# MAX DRAWDOWN
# =========================
def update_max_dd():

    curve = live_state.get("equity_curve", [])

    if len(curve) < 2:
        live_state["max_dd"] = 0
        return

    peak = curve[0]
    max_dd = 0

    for value in curve:

        if value > peak:
            peak = value

        dd = (peak - value) / peak

        if dd > max_dd:
            max_dd = dd

    live_state["max_dd"] = max_dd

def update_profits():
    trades = live_state.get("trades", [])

    total_profit = sum(
        t.get("pnl", 0) for t in trades
    )

    live_state["profits"] = total_profit