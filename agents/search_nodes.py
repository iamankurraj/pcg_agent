from asset_pipeline.local_search import search_local_assets
from asset_pipeline.web_search import search_web


ALLOWED_DOMAINS = [
    "fab.com"
]


def local_search_node(state):
    keywords = state.get("keywords", [])
    requested_type = state.get("asset_type")

    results = search_local_assets(keywords)

    # Filter by asset type if specified
    if requested_type:
        results = [
            r for r in results
            if r.get("type") == requested_type
        ]

    state["local_results"] = results
    return state


def web_search_node(state):
    query = state.get("cleaned_query", "")
    license_pref = state.get("license_preference", "any")

    # Only modify query if user explicitly wants free
    if license_pref == "free_only":
        query = f"{query} free OR CC0 OR Creative Commons"

    results = search_web(
        query=query,
        allowed_domains=ALLOWED_DOMAINS,
        license_preference=license_pref
    )

    state["web_results"] = results
    return state