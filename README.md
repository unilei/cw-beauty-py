# Cursor Beauty - AI Prompt Directory
# Cursor Beauty - AI 提示词目录

A curated collection of AI prompts for developers, built with Flask and MongoDB.
为开发者精心策划的 AI 提示词集合，使用 Flask 和 MongoDB 构建。

## Features | 功能特点

- User authentication and authorization | 用户认证和授权
- Prompt management (create, edit, delete) | 提示词管理（创建、编辑、删除）
- Admin dashboard for content moderation | 内容审核管理后台
- Markdown support for prompt content | 提示词内容支持 Markdown 格式
- Random avatar generation using DiceBear | 使用 DiceBear 生成随机头像
- Responsive design with Tailwind CSS | 使用 Tailwind CSS 的响应式设计
- AJAX-powered type and language switching | AJAX 驱动的类型和语言切换
- Search functionality | 搜索功能

## Tech Stack | 技术栈

- Backend: Flask
- Database: MongoDB (MongoEngine)
- Frontend: 
  - Tailwind CSS
  - Alpine.js
  - AJAX
- Authentication: Flask-Login
- Markdown: markdown2
- Avatar: DiceBear API

## Setup | 环境配置

1. Clone the repository | 克隆仓库
```bash
git clone [repository-url]
cd cursor-beauty
```

2. Install Python dependencies | 安装 Python 依赖
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies | 安装 Node.js 依赖
```bash
npm install
```

4. Set up environment variables | 设置环境变量
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Build CSS | 构建 CSS
```bash
npm run build:css  # For production | 生产环境
npm run watch:css  # For development | 开发环境
```

6. Run the application | 运行应用
```bash
flask run
```

## Project Structure | 项目结构

```
cursor-beauty/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── src/
│   │   └── images/
│   ├── templates/
│   ├── models/
│   └── routes/
├── requirements.txt
├── package.json
├── tailwind.config.js
└── README.md
```

## Models | 数据模型

- User: User authentication and profile management | 用户认证和档案管理
- Prompt: AI prompt content and metadata | AI 提示词内容和元数据
- Review: Content moderation system | 内容审核系统

## Routes | 路由

- `/`: Home page with prompt listing | 首页，显示提示词列表
- `/login`: User login | 用户登录
- `/register`: User registration | 用户注册
- `/settings`: User settings | 用户设置
- `/prompt/new`: Create new prompt | 创建新提示词
- `/prompt/<id>`: Prompt detail page | 提示词详情页
- `/admin`: Admin dashboard | 管理后台

## Frontend Features | 前端功能

### Tailwind CSS Configuration | Tailwind CSS 配置
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/src/**/*.js"
  ],
  // ... other configurations
}
```

### NPM Scripts | NPM 脚本
```json
{
  "scripts": {
    "build:css": "tailwindcss -i ./app/static/src/main.css -o ./app/static/css/main.css --minify",
    "watch:css": "tailwindcss -i ./app/static/src/main.css -o ./app/static/css/main.css --watch"
  }
}
```

## Contributing | 贡献指南

1. Fork the repository | 复刻仓库
2. Create your feature branch | 创建功能分支
3. Commit your changes | 提交更改
4. Push to the branch | 推送到分支
5. Create a Pull Request | 创建拉取请求

## License | 许可证

MIT License

## Contact | 联系方式

[Your contact information | 你的联系方式] 

## 部署指南

### 后端部署

1. 准备工作
```bash
# 克隆项目
git clone <your-repo-url>
cd cw-beauty-py

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

2. 环境变量配置
创建 `.env` 文件并配置以下变量：
```
MONGODB_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
FLASK_ENV=production
```

3. 数据库迁移
```bash
python migrations.py
```

4. 使用 Gunicorn 运行（生产环境）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 前端部署

1. 准备工作
```bash
cd frontend
npm install
```

2. 生产环境构建
```bash
# 修改 .env 文件设置后端API地址
echo "VITE_API_BASE_URL=https://your-api-domain.com" > .env

# 构建
npm run build
```

3. 部署选项：

#### 选项1：使用 Nginx 部署（同服务器）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 选项2：使用 Vercel 部署（推荐）

1. 在 Vercel 上导入你的 GitHub 仓库
2. 设置构建命令：
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
3. 添加环境变量 `VITE_API_BASE_URL`

### 使用 Docker 部署（可选）

1. 创建 Docker Compose 配置：

```yaml
version: '3'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/beauty_prompt
      - SECRET_KEY=your_secret_key
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

2. 运行 Docker Compose：
```bash
docker-compose up -d
```

## 部署检查清单

- [ ] 确保所有环境变量已正确配置
- [ ] 数据库连接已测试
- [ ] 前端API地址已正确设置
- [ ] CORS配置已正确设置
- [ ] 静态资源已正确部署
- [ ] SSL证书已配置（如需要）
- [ ] 数据库备份策略已制定
- [ ] 监控告警已配置

## 常见问题

1. 跨域问题：确保后端CORS配置正确
2. 静态资源404：检查nginx配置的root路径
3. 数据库连接失败：检查MongoDB连接字符串和网络配置
4. 前端API请求失败：确认API基础URL配置正确 