from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict, total=False):
    message: str
    cleaned_query: str
    keywords: List[str]
    asset_type: str
    license_preference: str
    priority: str

    local_results: List[Dict[str, Any]]
    web_results: List[Dict[str, Any]]

    best_source: str
    decision_reason: str
    final_results: List[Dict[str, Any]]

