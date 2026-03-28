# 阶段 1: 编译代码 (Build Stage)
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 阶段 2: 运行环境 (Production Stage)
FROM nginx:stable-alpine
# 将打包好的文件复制到 Nginx 目录
COPY --from=build /app/dist /usr/share/nginx/html
# 暴露 Nginx 默认端口
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]