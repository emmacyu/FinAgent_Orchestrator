# 路径：backend/Dockerfile
FROM python:3.11-slim

# 关键：更新包列表并安装 curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
# ... 后续的 COPY 和 pip install 保持不变

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存加速构建
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制业务代码
COPY . .

# 启动 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]