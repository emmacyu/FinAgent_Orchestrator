from typing import TypedDict, Optional, Annotated
import operator

class LoanState(TypedDict):
    # --- 基础输入数据 ---
    client_id: str  # 新增：用于 MCP 定位客户
    income: float
    debt: float

    # --- Risk Node 输出 ---
    risk_score: float
    risk_level: Optional[str]
    explanation: Optional[str]

    # --- Fraud Node 输出 ---
    fraud_flag: Optional[bool]
    fraud_reason: Optional[str]

    # --- Decision Node 输出 ---
    decision: Optional[str]
    status: Optional[str]

    # --- 核心：审计日志 (Lead 级必备) ---
    # Annotated[..., operator.add] 告诉 LangGraph：
    # 当多个节点返回 audit_log 时，请把它们 append 到列表里，而不是覆盖。
    audit_log: Annotated[list[str], operator.add]