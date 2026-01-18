#!/bin/bash
# 部署到服务器的脚本
# 使用方法：上传整个项目到服务器后执行此脚本

echo "========================================"
echo "🚀 热点抓取与爆文生成系统 - 部署脚本"
echo "========================================"
echo ""

# 1. 检查Python环境
echo "📋 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，正在安装..."
    sudo apt update
    sudo apt install -y python3 python3-pip
else
    echo "✅ Python3已安装: $(python3 --version)"
fi

# 2. 安装依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install flask flask-cors pymysql requests pandas beautifulsoup4

# 3. 安装Nginx（如果未安装）
echo ""
echo "🌐 检查Nginx..."
if ! command -v nginx &> /dev/null; then
    echo "正在安装Nginx..."
    sudo apt install -y nginx
fi

# 4. 配置Nginx反向代理
echo ""
echo "⚙️  配置Nginx..."

sudo tee /etc/nginx/sites-available/topic-generator > /dev/null <<'EOF'
server {
    listen 80;
    server_name 101.43.15.66;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/topic-generator/static;
        expires 30d;
    }
}
EOF

# 5. 启用配置
sudo ln -sf /etc/nginx/sites-available/topic-generator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 6. 创建systemd服务
echo ""
echo "🔧 创建系统服务..."

sudo tee /etc/systemd/system/topic-generator.service > /dev/null <<'EOF'
[Unit]
Description=Topic Generator Web Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/topic-generator
ExecStart=/usr/bin/python3 /var/www/topic-generator/run_web.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. 重载systemd
sudo systemctl daemon-reload

echo ""
echo "========================================"
echo "✅ 部署完成！"
echo "========================================"
echo ""
echo "🌍 访问地址："
echo "   http://101.43.15.66/"
echo ""
echo "📝 管理命令："
echo "   启动服务: sudo systemctl start topic-generator"
echo "   停止服务: sudo systemctl stop topic-generator"
echo "   重启服务: sudo systemctl restart topic-generator"
echo "   查看日志: sudo journalctl -u topic-generator -f"
echo "   开机启动: sudo systemctl enable topic-generator"
echo ""
echo "🔥 立即启动服务..."
sudo systemctl start topic-generator
sudo systemctl status topic-generator
echo ""
echo "✅ 服务已启动！"
