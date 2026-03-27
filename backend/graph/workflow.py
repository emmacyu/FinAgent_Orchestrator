from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.schemas.state import LoanState
from backend.agents.risk_agent import risk_agent_llm
from backend.agents.decision_agent import decision_agent
from backend.agents.fraud_agent import fraud_agent_llm
from langgraph.checkpoint.memory import MemorySaver
from backend.mcp.client import call_mcp_tool


async def risk_node(state: LoanState):
    # 1. 通过 MCP 获取核心信用上下文 (不再只看用户填写的 income/debt)
    credit_context = await call_mcp_tool(
        "get_client_credit_context", 
        {"client_id": state.get("client_id", "C001")}
    )
    
    # 2. 将背景数据传给你的 risk_agent_llm
    # 这样 LLM 就能做出基于真实历史数据的判定
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
    # 1. 调用 MCP 工具检查黑名单 (使用 client_id 或姓名，这里假设 mock 数据库有姓名)
    # 这里的 "name" 可以从 state 或之前的 context 中获取
    is_blacklisted = await call_mcp_tool(
        "check_fraud_blacklist", 
        {"name": state.get("client_name", "Unknown")} 
    )

    # 2. 将黑名单结果传给 LLM 或者是直接判定
    # 如果在黑名单，直接给 HIGH 风险
    if is_blacklisted is True:
        return {
            "fraud_flag": True,
            "fraud_reason": "MATCHED_INTERNAL_BLACKLIST",
            "audit_log": ["CRITICAL: Client found on internal fraud blacklist!"]
        }

    # 3. 否则，继续走原来的 LLM 逻辑
    result = fraud_agent_llm(state["income"], state["debt"], state["risk_score"])
    return {
        "fraud_flag": result["fraud_flag"], 
        "fraud_reason": result["reason"],
        "audit_log": ["Fraud check: Passed (No blacklist match)"]
    }


async def decision_node(state: LoanState):
    risk = state["risk_score"]
    fraud = state.get("fraud_flag", False)

    # 逻辑 A: 直接拒绝
    if risk > 0.7 or fraud:
        return {"decision": "REJECT", "status": "FINALIZED"}
    
    # 逻辑 B: 需要人工（核心：触发中断的标记）
    if risk > 0.4:
        return {"decision": "PENDING_HUMAN", "status": "WAITING"}

    # 逻辑 C: 直接通过
    return {"decision": "APPROVE", "status": "FINALIZED"}


def route_after_risk(state: LoanState):
    score = state["risk_score"]
    if score < 0.3: return "low"      # 低风险 -> 直接去 decision
    if score < 0.7: return "medium"   # 中风险 -> 必须去 fraud
    return "high"                     # 高风险 -> 直接去 decision (拒绝)


def route_after_decision(state: LoanState):
    # 如果是人工审核状态，我们让它流向一个特殊的逻辑或者 END
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
        "low": "decision",     # 低风险直接决策
        "medium": "fraud",     # 中风险走 fraud node
        "high": "decision"     # 高风险直接决策（可直接拒绝）
    }
)

graph.add_edge("fraud", "decision")

graph.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "wait": END,   # 配合 interrupt_after 使用
        "finish": END
    }
)

memory = MemorySaver()
# 重点：我们在 decision 节点执行完后中断，如果 decision 是 PENDING_HUMAN
app_graph = graph.compile(
    checkpointer=memory,
    interrupt_after=["decision"] 
)