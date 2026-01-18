#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web服务器启动脚本（简化版）
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 不修改stdout，直接导入并运行
if __name__ == '__main__':
    from web_server import app
    # 使用use_reloader=False避免stdout问题
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
