from pydantic import BaseModel


class LoanRequest(BaseModel):
    client_id: str  # for MCP queries
    income: float
    debt: float