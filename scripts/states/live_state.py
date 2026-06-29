live_state = {
    "starting_capital": 10000.0,
    "cash": 10000.0,
    "btc_holdings": 0.0,

    "current_price": 0.0,
    "previous_close": None,
    "entry_price": 0.0,
    "avg_entry_price": 0.0,

    "trades": [],
    "equity_curve": [],

    "candle_count": 0,

    "status": "STOPPED",
    "start_time": None,

    "portfolio_value": 0.0,
    "wins": 0,
    "losses": 0,
    "win_rate": 0.0,

    "sharpe_ratio": 0.0,
    "max_dd": 0.0,
    "profits": 0.0,

    "df": None,
    "last_dca_price": 0.0,
    "dca_count": 0,

    # will be filled later dynamically
    "state_summary": None,
    "selected_strategy": "DAY",
}