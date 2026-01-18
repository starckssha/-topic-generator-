#!/bin/bash
cd /var/www/topic-generator

# 停止旧进程
pkill -f 'python3 run_web.py' || true
sleep 2

# 启动服务
nohup python3 run_web.py > server.log 2>&1 &

sleep 3

# 检查状态
if ps aux | grep -v grep | grep 'python3 run_web.py' > /dev/null; then
    echo "✓ 服务启动成功"
    ps aux | grep -v grep | grep 'python3 run_web.py'
    echo ""
    echo "日志（最后10行）:"
    tail -10 server.log
else
    echo "✗ 服务启动失败"
    tail -20 server.log
    exit 1
fi
