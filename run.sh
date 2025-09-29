#!/bin/bash

# AI招聘筛选助手启动脚本

echo "🚀 AI招聘筛选助手启动脚本"
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  环境变量文件不存在，正在创建..."
    cp env.txt .env
    echo "📝 请编辑.env文件，设置智谱清言API密钥"
    echo "   ZHIPU_API_KEY=your_zhipu_api_key_here"
    read -p "按回车键继续..."
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p uploads
mkdir -p nginx/ssl
mkdir -p logs

# 设置权限
chmod 755 uploads
chmod 755 logs

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose build

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 健康检查
echo "🏥 进行健康检查..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务启动失败"
    docker-compose logs backend
    exit 1
fi

if curl -f http://localhost:3000 &> /dev/null; then
    echo "✅ 前端服务运行正常"
else
    echo "❌ 前端服务启动失败"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 AI招聘筛选助手启动成功！"
echo "================================"
echo "📱 前端界面: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "📋 管理命令："
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo "   查看状态: docker-compose ps"
echo ""
echo "💡 提示：首次使用请确保已配置智谱清言API密钥"
