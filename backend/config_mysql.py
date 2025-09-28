"""
MySQL数据库配置示例
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL数据库配置
DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', 'password')}@{os.getenv('MYSQL_HOST', 'localhost')}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE', 'recruitment_assistant')}"

# 其他配置保持不变...
