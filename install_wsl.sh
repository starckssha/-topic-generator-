#!/bin/bash
echo "=== WSL2 环境设置 ==="
echo ""

# 更新包管理器
sudo apt-get update

# 安装Python 3和pip
sudo apt-get install -y python3 python3-pip

# 显示版本
python3 --version

# 安装requests
pip3 install requests

echo ""
echo "=== 安装完成 ==="
