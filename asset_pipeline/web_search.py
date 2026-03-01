import os
from tavily import TavilyClient
from urllib.parse import urlparse


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY)


def domain_allowed(url: str, allowed_domains):
    if not allowed_domains:
        return True

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    return any(allowed.lower() in domain for allowed in allowed_domains)


def search_web(query: str, allowed_domains=None, license_preference="any"):
    """
    Search web with optional strict domain restriction
    and optional free-only filtering.
    """

    if not TAVILY_API_KEY:
        return [{"error": "TAVILY_API_KEY not set."}]

    search_params = {
        "query": query + " unreal engine asset download",
        "search_depth": "advanced",
        "max_results": 10
    }

    if allowed_domains:
        search_params["include_domains"] = allowed_domains

    response = client.search(**search_params)

    results = []

    for item in response.get("results", []):

        url = item.get("url")

        # 🔒 HARD DOMAIN FILTER
        if not domain_allowed(url, allowed_domains):
            continue

        results.append({
            "title": item.get("title"),
            "url": url,
            "content_snippet": item.get("content")[:300] if item.get("content") else "",
            "score": item.get("score")
        })

        # 🔥 FREE FILTER (ONLY WHEN USER REQUESTS)
    if license_preference == "free_only":
        filtered = []

        for r in results:
            combined = (r["title"] + " " + r["content_snippet"]).lower()

            if (
                "free" in combined
                or "creative commons" in combined
                or "cc-" in combined
                or "cc by" in combined
            ):
                filtered.append(r)

        results = filtered
    return results