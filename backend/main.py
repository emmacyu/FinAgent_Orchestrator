import uuid
from fastapi import FastAPI, HTTPException
from backend.graph.workflow import app_graph
from backend.schemas.request import LoanRequest
from fastapi.middleware.cors import CORSMiddleware  # 导入中间件


app = FastAPI()

# 定义允许访问的源
origins = [
    "http://localhost:3000",   # Docker Nginx 映射端口
    "http://127.0.0.1:3000",   # 备用
    "http://localhost:5173",   # 保留 Vite 开发端口
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 只有这些源可以访问
    allow_credentials=True,           # 允许携带 Cookie（如果以后需要登录）
    allow_methods=["*"],              # 允许所有方法 (GET, POST, OPTIONS 等)
    allow_headers=["*"],              # 允许所有请求头
)

@app.post("/risk")
async def calculate_risk(request: LoanRequest): # 这里的 'request' 是变量名，类型必须是 'LoanRequest'
    # 打印收到的数据，方便你在终端查看
    print(f"Received Request: {request.dict()}") 

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    try:
        # 确保传入的是字典：request.dict()
        result = await app_graph.ainvoke(request.dict(), config=config)
        return result
    except Exception as e:
        print(f"Graph Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
