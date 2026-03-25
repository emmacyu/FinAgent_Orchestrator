from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.schemas.state import LoanState
from backend.agents.risk_agent import risk_agent_llm
from backend.agents.decision_agent import decision_agent
from backend.agents.fraud_agent import fraud_agent_llm


class GraphState(TypedDict):
    income: float
    debt: float

    risk_score: float
    risk_level: str
    explanation: str

    fraud_flag: bool
    fraud_reason: str


def risk_node(state: LoanState):
    result = risk_agent_llm(state["income"], state["debt"])
    return {**state, **result}


def fraud_node(state: GraphState):
    result = fraud_agent_llm(
        state["income"],
        state["debt"],
        state["risk_score"]
    )

    return {
        "fraud_flag": result["fraud_flag"],
        "fraud_reason": result["reason"]
    }


def decision_node(state: GraphState):
    risk = state["risk_score"]
    fraud = state["fraud_flag"]

    if fraud:
        decision = "REJECT"
    elif risk > 0.7:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return {"decision": decision}


graph = StateGraph(LoanState)

graph.add_node("risk", risk_node)
graph.add_node("fraud", fraud_node)
graph.add_node("decision", decision_node)

graph.set_entry_point("risk")

graph.add_edge("risk", "fraud")
graph.add_edge("fraud", "decision")
graph.add_edge("decision", END)

app_graph = graph.compile()