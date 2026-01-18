#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI图片生成服务 - 根据文字生成配图
"""
import os
import sys
import requests
from datetime import datetime

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 图片输出目录
IMAGE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'generated_images')
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)


def generate_image_with_dalle(title, content):
    """
    使用DALL-E生成图片（需要OpenAI API）

    Args:
        title: 文章标题
        content: 文章内容

    Returns:
        图片URL或None
    """
    try:
        import openai

        # 设置API Key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None

        openai.api_key = api_key

        # 生成图片提示词
        prompt = f"为这篇小红书笔记生成配图：\n标题：{title}\n内容摘要：{content[:200]}\n\n风格：现代简约、教育科技感、色彩鲜明"

        # 调用DALL-E
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']

        return image_url

    except ImportError:
        return None
    except Exception as e:
        return None


def generate_image_with_stability(title, content):
    """
    使用Stability AI生成图片

    Args:
        title: 文章标题
        content: 文章内容

    Returns:
        图片URL或None
    """
    try:
        api_key = os.getenv('STABILITY_API_KEY')
        if not api_key:
            return None

        # 生成图片提示词
        prompt = f"Education technology, AI learning, modern illustration, {title[:50]}"

        # 调用Stability AI API
        url = "https://api.stability.ai/v1/generation/text-to-image"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": 30,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

        # 保存图片
        image_data = result['artifacts'][0]['base64']
        import base64
        image_bytes = base64.b64decode(image_data)

        filename = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(IMAGE_OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # 返回图片URL（需要配置图片服务器）
        image_url = f"http://192.168.31.8:5000/static/generated_images/{filename}"
        return image_url

    except Exception as e:
        return None


def generate_image_placeholder(title):
    """
    生成占位图片URL（用于测试）

    Args:
        title: 文章标题

    Returns:
        占位图片URL
    """
    # 使用免费的占位图片服务
    # 可以替换成实际的图片生成API

    options = [
        f"https://placehold.co/600x400/667eea/white?text={title[:10]}",
        f"https://via.placeholder.com/600x400/667eea/ffffff?text={title[:10]}",
    ]

    return options[0]


def generate_image_for_post(post_title, post_content, method='placeholder'):
    """
    为文章生成配图

    Args:
        post_title: 文章标题
        post_content: 文章内容
        method: 生成方法 ('dalle', 'stability', 'placeholder')

    Returns:
        图片URL
    """
    if method == 'dalle':
        image_url = generate_image_with_dalle(post_title, post_content)
    elif method == 'stability':
        image_url = generate_image_with_stability(post_title, post_content)
    else:
        image_url = generate_image_placeholder(post_title)

    return image_url


if __name__ == '__main__':
    # 测试生成图片
    title = "震惊数学界！AI自动解决30年难题"
    content = "这是一个测试内容..."

    print("测试图片生成功能\n")

    # 使用占位符模式（无需API Key）
    url = generate_image_for_post(title, content, method='placeholder')
    print(f"\n生成的图片URL: {url}")

    print("\n" + "="*70)
    print("💡 提示:")
    print("1. 如需使用真实AI生成，设置环境变量:")
    print("   export OPENAI_API_KEY=your_key  # DALL-E")
    print("   export STABILITY_API_KEY=your_key  # Stability AI")
    print()
    print("2. 然后修改method='dalle'或method='stability'")
    print("="*70)
