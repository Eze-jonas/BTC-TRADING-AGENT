from scripts.states.live_state import live_state
from datetime import datetime

system_running = False


def start_live_system():
    global system_running
    system_running = True

    live_state["status"] = "RUNNING"
    live_state["start_time"] = datetime.utcnow()


def stop_live_system():
    global system_running
    system_running = False
    live_state["status"] = "STOPPED"


def get_system_status():
    return {
        "status": live_state.get("status", "STOPPED"),
        "running_flag": system_running
    }