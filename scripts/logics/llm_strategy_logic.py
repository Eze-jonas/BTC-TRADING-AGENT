from scripts.states.live_state import live_state


def run_llm_strategy(llm, market_summary, state_summary, regime):
    llm_result = llm.choose_strategy(market_summary)

    print("🤖 LLM RAW RESULT:", llm_result)

    llm_strategy = llm_result["strategy"]

    print("🎯 LLM STRATEGY SELECTED:", llm_strategy)

    live_state["llm_strategy"] = llm_strategy
    live_state["rule_strategy"] = None  # optional

    final_strategy = llm_strategy
    live_state["selected_strategy"] = final_strategy

    print("🚦 FINAL STRATEGY USED:", final_strategy)

    print("STATE SUMMARY:", state_summary)
    print("🚦 REGIME:", regime)
    print("🎯 ROUTED STRATEGY:", live_state["selected_strategy"])

    return final_strategy