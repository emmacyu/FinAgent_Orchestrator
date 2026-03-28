# 路径：backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存加速构建
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制业务代码
COPY . .

# 启动 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]