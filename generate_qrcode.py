#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成小红书爆文发布系统的二维码
"""
import os
import sys
import qrcode
from PIL import Image
import urllib.parse

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置
SERVER_URL = "http://localhost:5000/h5/index.html"  # 本地测试
# SERVER_URL = "http://your-domain.com/h5/index.html"  # 生产环境（请替换为您的域名）

def generate_qrcode(url, filename, size=300):
    """
    生成二维码

    Args:
        url: 二维码内容
        filename: 保存文件名
        size: 二维码尺寸
    """
    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)

    # 生成图片
    img = qr.make_image(fill_color="black", back_color="white")

    # 调整大小
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # 保存
    img.save(filename)
    print(f"✅ 二维码已生成: {filename}")

    return filename


def main():
    """主函数"""
    print("="*70)
    print("🔥 小红书爆文发布系统 - 二维码生成工具")
    print("="*70)
    print()

    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # 生成主页二维码
    print("生成主页二维码...")
    main_qr = os.path.join(output_dir, 'xiaohongshu_app_qrcode.png')
    generate_qrcode(SERVER_URL, main_qr, size=400)

    # 生成不同尺寸的二维码
    print("\n生成不同尺寸的二维码...")
    sizes = {
        'xiaohongshu_qrcode_small.png': 200,
        'xiaohongshu_qrcode_medium.png': 300,
        'xiaohongshu_qrcode_large.png': 500
    }

    for filename, size in sizes.items():
        filepath = os.path.join(output_dir, filename)
        generate_qrcode(SERVER_URL, filepath, size=size)

    print()
    print("="*70)
    print("✅ 所有二维码生成完成！")
    print("="*70)
    print()
    print("📱 使用说明:")
    print("1. 启动后端服务: python app_flask.py")
    print(f"2. 访问URL: {SERVER_URL}")
    print("3. 用手机扫描二维码即可访问")
    print()
    print("📂 二维码文件位置:")
    print(f"   {output_dir}/xiaohongshu_qrcode_*.png")
    print()
    print("="*70)


if __name__ == '__main__':
    # 检查依赖
    try:
        import qrcode
        from PIL import Image
    except ImportError:
        print("❌ 缺少依赖库，请先安装:")
        print("   pip install qrcode pillow")
        exit(1)

    main()
