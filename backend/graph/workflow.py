# ...existing code...
from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.schemas.state import LoanState
from backend.agents.risk_agent import risk_agent_llm
from backend.agents.decision_agent import decision_agent
from backend.agents.fraud_agent import fraud_agent_llm
from langgraph.checkpoint.memory import MemorySaver
from backend.mcp.client import call_mcp_tool


async def risk_node(state: LoanState):
    # 1. Retrieve core credit context via MCP (no longer only looking at user-provided income/debt)
    credit_context = await call_mcp_tool(
        "get_client_credit_context",
        {"client_id": state.get("client_id", "C001")}
    )

    # 2. Pass the background data to risk_agent_llm
    # This allows the LLM to make judgments based on real historical data
    result = risk_agent_llm(
        income=state["income"], 
        debt=state["debt"],
        external_context=credit_context
    )

    return {
        "risk_score": result["risk_score"],
        "audit_log": [f"Risk analysis with MCP Context: {credit_context}"]
    }


async def fraud_node(state: LoanState):
    # 1. Call the MCP tool to check the blacklist (use client_id or name; assume mock DB has names)
    # The "name" here can be obtained from state or previous context
    is_blacklisted = await call_mcp_tool(
        "check_fraud_blacklist", 
        {"name": state.get("client_name", "Unknown")} 
    )

    # 2. Pass the blacklist result to the LLM or decide directly
    # If on the blacklist, mark as HIGH risk immediately
    if is_blacklisted is True:
        return {
            "fraud_flag": True,
            "fraud_reason": "MATCHED_INTERNAL_BLACKLIST",
            "audit_log": ["CRITICAL: Client found on internal fraud blacklist!"]
        }

    # 3. Otherwise, continue with the original LLM logic
    result = fraud_agent_llm(state["income"], state["debt"], state["risk_score"])
    return {
        "fraud_flag": result["fraud_flag"], 
        "fraud_reason": result["reason"],
        "audit_log": ["Fraud check: Passed (No blacklist match)"]
    }


async def decision_node(state: LoanState):
    risk = state["risk_score"]
    fraud = state.get("fraud_flag", False)

    # Logic A: immediate rejection
    if risk > 0.7 or fraud:
        return {"decision": "REJECT", "status": "FINALIZED"}
    
    # Logic B: require human review (core: trigger an interrupt flag)
    if risk > 0.4:
        return {"decision": "PENDING_HUMAN", "status": "WAITING"}

    # Logic C: immediate approval
    return {"decision": "APPROVE", "status": "FINALIZED"}


def route_after_risk(state: LoanState):
    score = state["risk_score"]
    if score < 0.3: return "low"      # low risk -> go directly to decision
    if score < 0.7: return "medium"   # medium risk -> must go to fraud
    return "high"                     # high risk -> go directly to decision (likely reject)


def route_after_decision(state: LoanState):
    # If it's pending human review, route to a special flow or END
    if state["decision"] == "PENDING_HUMAN":
        return "wait"
    return "finish"


graph = StateGraph(LoanState)

graph.add_node("risk", risk_node)
graph.add_node("fraud", fraud_node)
graph.add_node("decision", decision_node)

graph.set_entry_point("risk")

graph.add_conditional_edges(
    "risk",
    route_after_risk,
    {
        "low": "decision",     # low risk directly to decision
        "medium": "fraud",     # medium risk goes to fraud node
        "high": "decision"     # high risk directly to decision (can be rejected)
    }
)

graph.add_edge("fraud", "decision")

graph.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "wait": END,   # used with interrupt_after
        "finish": END
    }
)

memory = MemorySaver()
# Important: we interrupt after the decision node if the decision is PENDING_HUMAN
app_graph = graph.compile(
    checkpointer=memory,
    interrupt_after=["decision"]
)