"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 智谱清言API配置
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "your_zhipu_api_key_here")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 数据库配置
import os
DATABASE_URL = f"sqlite:///{os.path.abspath('recruitment_assistant.db')}"

# 文件上传配置
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

# 应用配置
APP_NAME = "AI招聘筛选助手"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS配置
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173"
]
