"""
FastAPI主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import init_database
from config import APP_NAME, APP_VERSION, CORS_ORIGINS
from api import upload, process, report
import os

# 创建FastAPI应用
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="基于智谱清言API的智能招聘筛选系统",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(upload.router)
app.include_router(process.router)
app.include_router(report.router)

# 创建uploads目录
os.makedirs("uploads", exist_ok=True)

# 提供静态文件服务（用于文件下载）
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {APP_NAME} v{APP_VERSION} 启动中...")
    init_database()
    print("✅ 数据库初始化完成")
    print("📁 文件上传目录已创建")
    print("🌐 API文档地址: http://localhost:8000/docs")

@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径，返回简单的欢迎页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI招聘筛选助手</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
            .logo { font-size: 2.5em; color: #007bff; margin-bottom: 20px; }
            .description { color: #666; margin-bottom: 30px; }
            .links a { display: inline-block; margin: 10px; padding: 10px 20px; 
                      background: #007bff; color: white; text-decoration: none; 
                      border-radius: 5px; }
            .links a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🤖 AI招聘筛选助手</div>
            <div class="description">
                基于智谱清言API的智能招聘筛选系统<br>
                自动分析简历匹配度，生成个性化面试问题和分析报告
            </div>
            <div class="links">
                <a href="/docs">📚 API文档</a>
                <a href="/redoc">📖 ReDoc文档</a>
                <a href="http://localhost:5173" target="_blank">🎨 前端界面</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "message": "服务运行正常"
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404错误处理"""
    return HTTPException(
        status_code=404,
        detail={
            "error": "资源不存在",
            "message": "请求的资源未找到",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """500错误处理"""
    return HTTPException(
        status_code=500,
        detail={
            "error": "服务器内部错误",
            "message": "请稍后重试或联系管理员",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动AI招聘筛选助手...")
    print("📝 配置信息:")
    print(f"   - 应用名称: {APP_NAME}")
    print(f"   - 版本: {APP_VERSION}")
    print(f"   - 调试模式: {os.getenv('DEBUG', 'False')}")
    print(f"   - API文档: http://localhost:8000/docs")
    print(f"   - 前端地址: http://localhost:5173")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
