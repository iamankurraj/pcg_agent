from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.decision_agent import analyze_request
from agents.license_agent import analyze_license
from agents.strategy_agent import analyze_strategy
from agents.search_nodes import local_search_node, web_search_node
from agents.ranking_agent import rank_results


def build_graph():

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("intent", analyze_request)
    workflow.add_node("license", analyze_license)
    workflow.add_node("strategy", analyze_strategy)
    workflow.add_node("local_search", local_search_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("ranking", rank_results)

    # Entry
    workflow.set_entry_point("intent")

    # Linear flow
    workflow.add_edge("intent", "license")
    workflow.add_edge("license", "strategy")
    workflow.add_edge("strategy", "local_search")

    # Conditional after local search
    def decide_next(state):
        priority = state.get("priority")
        local_results = state.get("local_results") or []

        # If user prefers local and we have local matches,
        # skip web and go straight to ranking
        if priority == "local_first" and local_results:
            return "ranking"

        # Otherwise always go to web search
        return "web_search"

    workflow.add_conditional_edges(
        "local_search",
        decide_next,
        {
            "ranking": "ranking",
            "web_search": "web_search",
        }
    )

    # Web always followed by ranking
    workflow.add_edge("web_search", "ranking")

    # Ranking is always final
    workflow.add_edge("ranking", END)

    return workflow.compile()