#!/bin/bash
# 完整部署脚本 - 一键启动内容生成器

echo "========================================="
echo "  内容生成器 - 部署脚本"
echo "========================================="
echo ""

# 1. 配置Nginx
echo "[1/4] 配置Nginx反向代理..."
cat > /etc/nginx/sites-available/topic-generator << 'NGINX_CONFIG'
server {
    listen 80;
    server_name 101.43.15.66;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
NGINX_CONFIG

# 2. 启用Nginx配置
echo "[2/4] 启用Nginx配置..."
ln -sf /etc/nginx/sites-available/topic-generator /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# 3. 启动Flask服务
echo "[3/4] 启动Flask服务..."
cd /var/www/topic-generator

# 停止旧进程
pkill -f 'python3 run_web.py' 2>/dev/null
sleep 2

# 启动新进程
nohup python3 run_web.py > server.log 2>&1 &
sleep 3

# 4. 检查服务状态
echo "[4/4] 检查服务状态..."
echo ""

if ps aux | grep -v grep | grep 'python3 run_web.py' > /dev/null; then
    echo "✓ Flask服务已启动"
    echo ""
    echo "进程信息:"
    ps aux | grep -v grep | grep 'python3 run_web.py'
    echo ""
    echo "端口监听:"
    netstat -tlnp | grep :5000
    echo ""
    echo "========================================="
    echo "  ✅ 部署成功！"
    echo "========================================="
    echo ""
    echo "🌍 访问地址: http://101.43.15.66/"
    echo ""
    echo "查看日志: tail -f /var/www/topic-generator/server.log"
else
    echo "✗ Flask服务启动失败"
    echo ""
    echo "错误日志:"
    tail -30 /var/www/topic-generator/server.log
    exit 1
fi
