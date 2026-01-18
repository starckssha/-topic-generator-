#!/bin/bash
# 部署脚本 - 同步代码到生产服务器

SERVER="root@101.43.15.66"
SERVER_DIR="/root/topicgenerator"

echo "🚀 开始部署到服务器 $SERVER..."

# 1. 创建远程目录
echo "📁 创建远程目录..."
ssh $SERVER "mkdir -p $SERVER_DIR"

# 2. 同步代码 (排除不必要的文件)
echo "📦 同步代码文件..."
rsync -avz --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='output' \
    --exclude='data' \
    --exclude='*.log' \
    --exclude='scripts' \
    --exclude='test_*.py' \
    ./ $SERVER:$SERVER_DIR/

# 3. 运行数据库迁移脚本
echo "🗄️ 运行数据库迁移..."
ssh $SERVER "cd $SERVER_DIR && python3 scripts/add_first_generated_at.py"

# 4. 重启服务
echo "🔄 重启服务..."
ssh $SERVER "cd $SERVER_DIR && pkill -f 'python.*web_server.py' 2>/dev/null; nohup python3 web_server.py > server.log 2>&1 &"

# 5. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 3

# 6. 测试服务
echo "🧪 测试服务..."
ssh $SERVER "curl -s http://localhost:5000/api/generate/available-topics?limit=1 | head -100"

echo ""
echo "✅ 部署完成!"
echo "📊 访问: http://101.43.15.66/"
