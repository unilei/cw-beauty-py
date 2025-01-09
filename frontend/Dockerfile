FROM node:18-alpine as build-stage

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# 设置工作目录
WORKDIR /app

# 设置 Docker 环境变量
ENV DOCKER_ENV=true

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产阶段 - 使用轻量级服务器
FROM node:18-alpine

# 安装调试工具
RUN apk add --no-cache curl iputils busybox-extras

WORKDIR /app

# 安装 serve 包来提供静态文件服务
RUN npm install -g serve

# 从构建阶段复制构建文件
COPY --from=build-stage /app/dist ./dist

EXPOSE 3000

# 使用 serve 启动静态文件服务
CMD ["serve", "-s", "dist", "-l", "3000"] 