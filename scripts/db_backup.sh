#!/bin/bash

# 数据库备份脚本

echo "🗄️  AI招聘筛选助手数据库备份脚本"
echo "=================================="

# 创建备份目录
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# 生成备份文件名
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/recruitment_assistant_$TIMESTAMP.db"

# 备份SQLite数据库
if [ -f "backend/recruitment_assistant.db" ]; then
    cp backend/recruitment_assistant.db $BACKUP_FILE
    echo "✅ 数据库备份成功: $BACKUP_FILE"
else
    echo "❌ 数据库文件不存在: backend/recruitment_assistant.db"
    exit 1
fi

# 备份上传文件
if [ -d "backend/uploads" ]; then
    UPLOAD_BACKUP="$BACKUP_DIR/uploads_$TIMESTAMP"
    cp -r backend/uploads $UPLOAD_BACKUP
    echo "✅ 上传文件备份成功: $UPLOAD_BACKUP"
fi

echo ""
echo "📋 备份文件列表:"
ls -la $BACKUP_DIR/

echo ""
echo "💡 恢复命令:"
echo "   cp $BACKUP_FILE backend/recruitment_assistant.db"
