from agents.intent_agent import extract_keywords
from asset_pipeline.local_search import search_local_assets

query = "pine tree"

keywords = extract_keywords(query)
results = search_local_assets(keywords)

for r in results[:5]:
    print(r)