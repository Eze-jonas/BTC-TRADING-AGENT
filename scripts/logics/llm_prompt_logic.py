import json
import ollama
from scripts.configurations.parameter_configuration import config


class LLMWrapper:
    def __init__(self, model=None):
        self.model = model or config["llm_model"]

    def choose_strategy(self, market_summary):

        prompt = f"""
You are an expert Bitcoin trading strategist.

Current Market Summary:

{json.dumps(market_summary, indent=2)}

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
                "temperature": config["llm_temperature"]
            }
        )

        raw_output = response["message"]["content"]

        # Safe JSON parsing
        try:
            result = json.loads(raw_output)
        except Exception:
            import re

            json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)

            result = (
                json.loads(json_match.group())
                if json_match
                else {
                    "strategy": "DAY",
                    "reason": "fallback due to parsing error"
                }
            )

        print("\n==============================")
        print("LLM STRATEGY DECISION")
        print("==============================")
        print("Strategy :", result["strategy"])
        print("Reason   :", result["reason"])
        print("==============================\n")

        return result