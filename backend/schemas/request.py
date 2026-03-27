from pydantic import BaseModel


class LoanRequest(BaseModel):
    client_id: str  # 必须传入，用于 MCP 查询
    income: float
    debt: float