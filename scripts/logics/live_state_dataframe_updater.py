import pandas as pd

from scripts.states.live_state import live_state


def update_live_state_dataframe(candle):

    current_df = live_state["df"]

    new_row = pd.DataFrame([candle]).set_index("open_time")

    updated_df = pd.concat([current_df, new_row])

    updated_df = updated_df.tail(500)

    live_state["df"] = updated_df