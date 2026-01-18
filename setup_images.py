#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片服务器配置工具
帮助用户设置本地图片服务器并生成公网可访问的URL
"""
import os
import shutil

def setup_image_server():
    """配置图片服务器"""
    print("="*70)
    print("🖼️  小红书爆文发布系统 - 图片服务器配置")
    print("="*70)
    print()

    # 创建图片目录
    image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    os.makedirs(image_dir, exist_ok=True)

    print(f"✅ 图片目录已创建: {image_dir}")
    print()

    # 创建示例图片说明
    readme_content = """# 图片服务器使用说明

## 📁 目录位置
static/images/

## 🖼️  支持的图片格式
- JPG / JPEG
- PNG
- GIF
- WebP

## 📤 如何添加图片

### 方式1: 直接复制
将图片文件复制到 `static/images/` 目录

### 方式2: 使用脚本
```bash
python copy_images.py
```

## 🌐 访问URL格式

### 本地访问
http://localhost:5000/static/images/your-image.jpg

### 公网访问（需要内网穿透）
使用ngrok或frp等工具生成公网URL后:
https://your-domain.ngrok.io/static/images/your-image.jpg

## ⚠️  注意事项
1. 图片文件名建议使用英文，避免中文和特殊字符
2. 图片大小建议控制在2MB以内
3. 小红书分享API需要公网可访问的图片URL
4. 如果使用本地测试，可以先不配置图片，只分享文字内容

## 🔧 内网穿透工具推荐
- **ngrok**: https://ngrok.com/ (简单易用)
- **frp**: https://github.com/fatedier/frp (功能强大)
- **cpolar**: https://www.cpolar.com/ (国内访问快)
"""

    readme_path = os.path.join(image_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ 说明文档已创建: {readme_path}")
    print()

    # 创建示例图片占位符
    placeholder_content = """这是一个图片占位符文件。

请将您的实际图片放到此目录下。

示例图片命名:
- cover_1.jpg (封面图1)
- cover_2.jpg (封面图2)
- education_1.jpg (教育相关)
- ai_learning.jpg (AI学习场景)
"""

    placeholder_path = os.path.join(image_dir, '图片占位符.txt')
    with open(placeholder_path, 'w', encoding='utf-8') as f:
        f.write(placeholder_content)

    print(f"✅ 占位符文件已创建: {placeholder_path}")
    print()

    print("="*70)
    print("✅ 图片服务器配置完成！")
    print("="*70)
    print()
    print("📝 下一步操作:")
    print()
    print("1. 添加图片到 static/images/ 目录")
    print("2. 运行后端服务: python app_flask.py")
    print("3. 访问 http://localhost:5000/static/images/图片名.jpg 测试")
    print()
    print("🌐 如需公网访问（小红书分享需要）:")
    print()
    print("使用ngrok等内网穿透工具:")
    print("   ngrok http 5000")
    print()
    print("然后会生成一个公网URL，例如:")
    print("   https://abc123.ngrok.io")
    print()
    print("图片访问URL变为:")
    print("   https://abc123.ngrok.io/static/images/your-image.jpg")
    print()
    print("="*70)


if __name__ == '__main__':
    setup_image_server()
