# agents/ranking_agent.py

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rank_results(state):
    
    query = state.get("cleaned_query", "")
    license_pref = state.get("license_preference", "any")

    local_results = state.get("local_results") or []
    web_results = state.get("web_results") or []
    
    combined = local_results + web_results

    if not combined:
        state["final_results"] = []
        state["best_source"] = None
        state["decision_reason"] = "No results found."
        return state

    payload = {
        "query": query,
        "license_preference": license_pref,
        "results": combined
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """
You are a ranking agent.

Compare local Unreal assets and web results.
Ignore numeric scores.

Prefer:
- Specific matches over generic ones
- Assets that directly match query terms
- Free assets if query implies free/open source

If neither title nor name contains any major query keywords,
consider it irrelevant and penalize heavily.

Return JSON:

{
  "best_source": "local" | "web",
  "reason": string
}
"""
                },
                {
                    "role": "user",
                    "content": json.dumps(payload)
                }
            ],
            temperature=0
        )

        result = json.loads(response.choices[0].message.content)

        scored = result.get("ranked_results", [])

        # Attach scores
        for item in scored:
            idx = item["index"]
            combined[idx]["llm_score"] = item["score"]

        combined.sort(key=lambda x: x.get("llm_score", 0), reverse=True)

        state["final_results"] = combined[:5]
        state["best_source"] = "mixed"
        state["decision_reason"] = "Results ranked by LLM relevance scoring."

    except Exception as e:
        # Fallback: no crash
        state["final_results"] = combined[:5]
        state["best_source"] = "mixed"
        state["decision_reason"] = f"LLM ranking failed: {str(e)}"

    return state