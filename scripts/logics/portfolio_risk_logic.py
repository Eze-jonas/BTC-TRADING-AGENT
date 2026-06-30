from scripts.states.live_state import live_state
from scripts.configurations.parameter_configuration import config


def check_portfolio_safeguard():
    stop_value = live_state["starting_capital"] * (
        1 - config["portfolio_stop_pct"]
    )

    if live_state["portfolio_value"] <= stop_value:
        print("🛑 PORTFOLIO STOP TRIGGERED")
        print(f"Portfolio: ${live_state['portfolio_value']:.2f}")
        print(f"Stop Level: ${stop_value:.2f}")

        live_state["status"] = "PAUSED"
        return True

    return False