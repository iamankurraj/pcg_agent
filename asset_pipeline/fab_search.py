# import requests
# import json
# from urllib.parse import urlencode
# from bs4 import BeautifulSoup


# FAB_SEARCH = "https://www.fab.com/search"


# def build_fab_url(query, license_preference="any", sort_preference=None):

#     params = {"q": query}

#     if license_preference == "free_only":
#         params["is_free"] = 1

#     if sort_preference == "price_low_to_high":
#         params["sort_by"] = "price"

#     return f"{FAB_SEARCH}?{urlencode(params)}"


# def search_fab(query, license_preference="any", sort_preference=None):

#     url = build_fab_url(query, license_preference, sort_preference)

#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     r = requests.get(url, headers=headers)

#     soup = BeautifulSoup(r.text, "html.parser")

#     script = soup.find("script", {"id": "__NEXT_DATA__"})

#     if not script:
#         return []

#     data = json.loads(script.string)

#     results = []

#     try:
#         listings = (
#             data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["results"]
#         )

#         for item in listings:

#             title = item.get("title")
#             slug = item.get("slug")

#             results.append({
#                 "title": title,
#                 "url": f"https://www.fab.com/listings/{slug}",
#                 "source": "fab"
#             })

#     except Exception:
#         return []

#     return results[:10]