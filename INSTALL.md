# 安装部署指南

## 快速开始

### 方式一：Docker部署（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd recruitment-assistant
```

2. **配置环境变量**
```bash
cp env.txt .env
# 编辑.env文件，设置智谱清言API密钥
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端界面：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 方式二：本地开发部署

#### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

#### 后端部署

1. **进入后端目录**
```bash
cd backend
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp env.txt .env
# 编辑.env文件，设置智谱清言API密钥
```

5. **启动后端服务**
```bash
python main.py
```

#### 前端部署

1. **进入前端目录**
```bash
cd frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run dev
```

4. **构建生产版本**
```bash
npm run build
```

## 配置说明

### 环境变量配置

在项目根目录创建`.env`文件：

```bash
# 智谱清言API配置（必填）
ZHIPU_API_KEY=your_zhipu_api_key_here

# 应用配置
DEBUG=False
APP_NAME=AI招聘筛选助手
APP_VERSION=1.0.0

# 数据库配置
DATABASE_URL=sqlite:///./recruitment_assistant.db

# 文件上传配置
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=.pdf,.docx,.doc

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 智谱清言API配置

1. 访问[智谱清言开放平台](https://open.bigmodel.cn/)
2. 注册账号并获取API密钥
3. 在`.env`文件中设置`ZHIPU_API_KEY`

## 常见问题

### Q: 文件上传失败
A: 检查文件大小是否超过10MB，格式是否为PDF/DOCX/DOC

### Q: API调用失败
A: 检查智谱清言API密钥是否正确配置，网络连接是否正常

### Q: 前端页面无法访问
A: 检查后端服务是否正常启动，端口是否被占用

### Q: 数据库初始化失败
A: 检查数据库文件权限，确保有写入权限

## 生产环境部署

### 使用Docker Compose

1. **修改docker-compose.yml**
```yaml
# 根据需要修改端口映射
ports:
  - "80:80"  # 前端
  - "8000:8000"  # 后端
```

2. **配置HTTPS（可选）**
```bash
# 将SSL证书放入nginx/ssl目录
# 取消注释nginx.conf中的HTTPS配置
```

3. **启动生产服务**
```bash
docker-compose -f docker-compose.yml up -d
```

### 使用Nginx反向代理

1. **安装Nginx**
```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

2. **配置Nginx**
```bash
# 复制配置文件
sudo cp nginx/nginx.conf /etc/nginx/sites-available/recruitment-assistant
sudo ln -s /etc/nginx/sites-available/recruitment-assistant /etc/nginx/sites-enabled/
```

3. **重启Nginx**
```bash
sudo systemctl restart nginx
```

## 监控和维护

### 日志查看

```bash
# Docker日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 应用日志
tail -f backend/logs/app.log
```

### 数据库备份

```bash
# SQLite数据库备份
cp backend/recruitment_assistant.db backup/recruitment_assistant_$(date +%Y%m%d).db
```

### 性能优化

1. **启用Gzip压缩**
2. **配置CDN**
3. **使用Redis缓存**
4. **数据库索引优化**

## 更新升级

1. **备份数据**
```bash
cp backend/recruitment_assistant.db backup/
cp -r backend/uploads backup/
```

2. **更新代码**
```bash
git pull origin main
```

3. **重新构建**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

4. **验证服务**
```bash
curl http://localhost:8000/health
```

## 技术支持

如遇到问题，请检查：
1. 环境变量配置是否正确
2. 网络连接是否正常
3. 端口是否被占用
4. 日志文件中的错误信息

更多技术支持请参考项目README或提交Issue。
