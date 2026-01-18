#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Nano Banana 图片生成服务
使用 Gemini 2.5 Flash Image 模型生成高质量AI配图
"""
import os
import sys
import base64
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


def generate_image_with_nano_banana(title, content='', api_key=None):
    """
    使用 Google Gemini API (Nano Banana) 生成图片

    Args:
        title: 文章标题
        content: 文章内容（可选，用于生成更精准的图片）
        api_key: Google API Key（如果为None，从环境变量读取）

    Returns:
        图片URL或None
    """
    try:
        # 获取API Key
        if not api_key:
            api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')

        if not api_key:
            return None

        # 构建提示词（针对小红书教育类内容优化）
        prompt = f"""Generate a high-quality, eye-catching image for Xiaohongshu (Little Red Book) social media post.

Topic: {title}

Content context: {content[:200] if content else ''}

Requirements:
- Style: Modern, vibrant, educational technology theme
- Colors: Use gradient purple (#667eea) to blue (#764ba2) as primary colors
- Mood: Professional, inspiring, engaging
- Elements: Include subtle educational icons (books, AI brain, graduation cap, etc.)
- Text: Add the title "{title[:15]}" prominently in the image
- Layout: Clean and balanced, suitable for mobile scrolling
- Quality: High resolution, clear and crisp

The image should be visually appealing and encourage users to stop scrolling and read the content."""

        # Gemini API 端点
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"

        # 调用 API
        headers = {
            'Content-Type': 'application/json'
        }

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt}
                ]
            }],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            }
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        # 提取图片数据
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                for part in candidate['content']['parts']:
                    if 'inlineData' in part:
                        # 获取base64图片数据
                        image_data = part['inlineData']['data']

                        # 保存图片到本地
                        filename = f"nano_banana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        filepath = os.path.join(IMAGE_OUTPUT_DIR, filename)

                        # 解码并保存
                        image_bytes = base64.b64decode(image_data)
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)

                        # 返回本地URL
                        local_url = f"http://192.168.31.8:5000/static/generated_images/{filename}"
                        return local_url

        return None

    except Exception as e:
        print(f"[ERROR] Nano Banana generation failed: {str(e)}")
        return None


def generate_image_with_fallback(title, content=''):
    """
    生成图片，优先使用 Nano Banana，失败则使用占位图

    Args:
        title: 文章标题
        content: 文章内容

    Returns:
        图片URL
    """
    # 尝试使用 Nano Banana
    image_url = generate_image_with_nano_banana(title, content)

    # 如果失败，使用占位图
    if not image_url:
        print(f"[FALLBACK] Using placeholder image for: {title[:30]}")
        image_url = f"https://placehold.co/600x400/667eea/white?text={title[:10]}"

    return image_url


if __name__ == '__main__':
    # 测试生成
    print("="*70)
    print("🎨 Google Nano Banana 图片生成测试")
    print("="*70)
    print()

    title = "震惊数学界！AI自动解决30年难题"
    content = "AI技术突破，自动解决数学难题，陶哲轩教授都震惊了"

    print(f"标题: {title}")
    print(f"内容: {content}")
    print()
    print("⏳ 正在生成图片...")

    image_url = generate_image_with_fallback(title, content)

    print()
    print(f"✅ 图片生成完成！")
    print(f"🔗 URL: {image_url}")
    print()
    print("="*70)
    print()
    print("💡 提示:")
    print("1. 如需使用 Google API，请设置环境变量:")
    print("   set GOOGLE_API_KEY=your_api_key_here")
    print()
    print("2. 获取 API Key:")
    print("   访问 https://aistudio.google.com/app/apikey")
    print()
    print("3. 检查生成的图片:")
    print(f"   {image_url}")
    print("="*70)
