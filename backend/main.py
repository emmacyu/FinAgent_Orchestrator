from fastapi import FastAPI
from backend.graph.workflow import app_graph
from backend.schemas.request import LoanRequest

app = FastAPI()


@app.post("/risk")
def calculate_risk(request: LoanRequest):
    result = app_graph.invoke(request.dict())
    return {"result": result}