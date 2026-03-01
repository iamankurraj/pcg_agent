# agents/license_agent.py

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_license(state):

    message = state["message"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
Determine the license preference of the user.

Return JSON:

{
  "license_preference": "free_only" | "any" | "paid_only"
}
"""
            },
            {"role": "user", "content": message}
        ],
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)

    state["license_preference"] = result["license_preference"]

    return state