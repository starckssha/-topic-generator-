#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试公司API接口
"""
import os
import sys
import requests
import json

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 公司API地址
API_URL = "http://contenthub-test.applesay.cn/app-api/hotword/note-review/create"

# 测试数据（使用简单的英文避免编码问题）
test_data = {
    "title": "测试标题 - AI教育爆文发布系统",
    "content": "这是测试内容\n\n第一段\n第二段\n第三段",
    "tags": "AI教育,测试,发布",
    "noteImage": ""
}

def test_api():
    """测试API接口"""
    print("="*70)
    print("🧪 测试公司API接口")
    print("="*70)
    print()
    print(f"API地址: {API_URL}")
    print()
    print("发送测试数据...")
    print()

    try:
        # 发送POST请求
        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json'
            },
            json=test_data,
            timeout=30
        )

        print(f"状态码: {response.status_code}")
        print()

        if response.status_code == 200:
            print("✅ API调用成功！")
            print()
            print("响应内容:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("❌ API调用失败")
            print()
            print("响应内容:")
            print(response.text)

    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("请检查网络连接或API地址是否正确")

    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        print("请检查:")
        print("1. API地址是否正确")
        print("2. 网络连接是否正常")
        print("3. API服务是否正在运行")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

    print()
    print("="*70)


if __name__ == '__main__':
    test_api()
