import json
import ollama


class LLMWrapper:
    def __init__(self, model="llama3.1"):
        self.model = model

    def choose_strategy(self, market_summary):

        prompt = f"""
You are an expert Bitcoin trading strategist.

Current BTC Price: {market_summary["price"]}

Momentum: {market_summary["momentum"]}
SMA: {market_summary["sma"]}
RSI: {market_summary["rsi"]:.2f}
ATR: {market_summary["atr"]:.2f}
Market Regime: {market_summary["regime"]}

Current Position: {market_summary["position"]}
Cash Available: {market_summary["cash"]}
BTC Holdings: {market_summary["btc"]}

Choose the most appropriate trading strategy.

DAY:
- Best for strong trends
- Frequent entries and exits

SWING:
- Best for ranging or uncertain markets
- Longer holding periods

Return ONLY valid JSON:

{{
  "strategy": "DAY or SWING",
  "reason": "short explanation"
}}
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert trading strategist."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        raw_output = response["message"]["content"]

        # safe JSON parsing
        try:
            result = json.loads(raw_output)
        except Exception:
            # fallback if model returns extra text
            import re
            json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
            result = json.loads(json_match.group()) if json_match else {
                "strategy": "DAY",
                "reason": "fallback due to parsing error"
            }

        print("\n==============================")
        print("LLM STRATEGY DECISION")
        print("==============================")
        print("Strategy :", result["strategy"])
        print("Reason   :", result["reason"])
        print("==============================\n")

        return result