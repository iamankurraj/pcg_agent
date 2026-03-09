# # app/main.py

# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from agents.graph import build_graph
# from fastapi.staticfiles import StaticFiles



# load_dotenv()

# app = FastAPI()
# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
# # Build graph once at startup
# graph = build_graph()


# class SearchRequest(BaseModel):
#     message: str


# @app.post("/search")
# def search_assets(request: SearchRequest):

#     initial_state = {
#         "message": request.message
#     }

#     final_state = graph.invoke(initial_state)

#     return {
#         "analysis": {
#             "cleaned_query": final_state.get("cleaned_query"),
#             "asset_type": final_state.get("asset_type"),
#             "license_preference": final_state.get("license_preference"),
#             "priority": final_state.get("priority"),
#         },
#         "best_source": final_state.get("best_source"),
#         "decision_reason": final_state.get("decision_reason"),
#         "final_results": final_state.get("final_results", [])
#     }


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from agents.graph import build_graph

load_dotenv()

app = FastAPI()

# Enable CORS (for browser requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build graph once
graph = build_graph()


class SearchRequest(BaseModel):
    message: str


@app.post("/search")
def search_assets(request: SearchRequest):

    initial_state = {
        "message": request.message
    }

    final_state = graph.invoke(initial_state)

    return {
        "analysis": {
            "cleaned_query": final_state.get("cleaned_query"),
            "asset_type": final_state.get("asset_type"),
            "license_preference": final_state.get("license_preference"),
            "priority": final_state.get("priority"),
        },
        "best_source": final_state.get("best_source"),
        "decision_reason": final_state.get("decision_reason"),
        "final_results": final_state.get("final_results", [])
    }


# Serve UI AFTER API routes
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")