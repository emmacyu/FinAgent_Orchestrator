from pydantic import BaseModel


class LoanRequest(BaseModel):
    income: float
    debt: float