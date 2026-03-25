from typing import TypedDict


class LoanState(TypedDict):
    income: float
    debt: float
    risk_score: float
    risk_level: str
    explanation: str
    decision: str