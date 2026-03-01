import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_request(state):

    message = state.get("message", "")

    if not isinstance(message, str) or not message.strip():
        state["cleaned_query"] = ""
        state["keywords"] = []
        state["asset_type"] = None
        return state

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
Extract asset search intent.

Return JSON:

{
  "cleaned_query": string,
  "keywords": list of important keywords,
  "asset_type": "StaticMesh" | "Material" | "Texture" | null
}
"""
            },
            {"role": "user", "content": message}
        ],
        temperature=0
    )

    result = json.loads(response.choices[0].message.content)

    state["cleaned_query"] = result.get("cleaned_query", message)
    state["keywords"] = result.get("keywords", [])
    state["asset_type"] = result.get("asset_type")

    return state