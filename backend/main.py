import uuid
from fastapi import FastAPI, HTTPException
from backend.graph.workflow import app_graph
from backend.schemas.request import LoanRequest
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# define the allowed origins
origins = [
    "http://localhost:3000",   # Docker Nginx
    "http://127.0.0.1:3000",   # backup
    "http://localhost:5173",   # for Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # only the origins listed are allowed
    allow_credentials=True,           # allow credentials (if you need to log in later)
    allow_methods=["*"],              # allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # allow all headers
)

@app.post("/risk")
async def calculate_risk(request: LoanRequest):  # 'request' is of type 'LoanRequest'
    # print(f"Received Request: {request.dict()}")
    print(f"Received Request: {request.dict()}")

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    try:
        result = await app_graph.ainvoke(request.dict(), config=config)
        return result
    except Exception as e:
        print(f"Graph Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
