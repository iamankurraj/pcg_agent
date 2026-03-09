# agents/strategy_agent.py

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_strategy(state):

    query = state["cleaned_query"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
Decide search priority.

Return JSON:

{
  "priority": "local_first" | "web_first"
}
"""
            },
            {"role": "user", "content": query}
        ],
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)

    state["priority"] = result["priority"]

    return state
