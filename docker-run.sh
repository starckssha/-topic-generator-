#!/bin/bash
# Docker运行脚本

echo "========================================="
echo "Topic Generator - Docker运行环境"
echo "========================================="
echo ""

# 检查项目路径
PROJECT_PATH="/d/Projects/ClaudeCode/topicgenerater"

echo "[*] 项目路径: $PROJECT_PATH"
echo "[*] 当前目录:"
pwd
ls -la

echo ""
echo "[*] 拉取Python 3.11镜像..."
docker pull python:3.11-slim

echo ""
echo "[*] 在Docker容器中运行..."
echo ""

docker run --rm -it \
  -v "$PROJECT_PATH:/app" \
  -w /app \
  -e HTTP_PROXY=http://host.docker.internal:7897 \
  -e HTTPS_PROXY=http://host.docker.internal:7897 \
  python:3.11-slim bash -c "
    echo '[*] 安装依赖...'
    pip install requests -q
    
    echo ''
    echo '[*] 运行主程序...'
    echo ''
    python main.py
  "

echo ""
echo "[*] 完成！"
