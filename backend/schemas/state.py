from typing import TypedDict, Optional, Annotated
import operator

class LoanState(TypedDict):
    # --- basic inputs ---
    client_id: str  # for MCP queries
    income: float
    debt: float

    # --- Risk Node output ---
    risk_score: float
    risk_level: Optional[str]
    explanation: Optional[str]

    # --- Fraud Node output ---
    fraud_flag: Optional[bool]
    fraud_reason: Optional[str]

    # --- Decision Node output ---
    decision: Optional[str]
    status: Optional[str]

    # --- audit logs ---
    # Annotated[..., operator.add] tells LangGraph:
    # when multiple nodes return audit_log, they should be appended to the list instead of overwriting it.
    audit_log: Annotated[list[str], operator.add]