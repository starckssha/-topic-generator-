#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将现有的小红书爆文Markdown转换为CSV格式
"""
import os
import sys
import csv
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.exporter_csv import CSVExporter


def parse_xiaohongshu_md(filepath):
    """解析小红书爆文Markdown文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    posts = []
    sections = content.split('## 爆文')

    for section in sections[1:]:  # 跳过第一个空section
        lines = section.strip().split('\n')

        # 提取爆文编号和标题
        title_line = lines[0]
        post_num = title_line.split(':')[0].strip()
        post_title = ':'.join(title_line.split(':')[1:]).strip() if ':' in title_line else ''

        # 提取元数据
        original_topic = ''
        platform = ''
        hot_value = ''

        for line in lines:
            if '**原热点：**' in line or '**原热点**' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    original_topic = parts[1].strip().strip('"').strip('*').strip()
            elif '**平台：**' in line or '**平台**' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    platform_info = parts[1].strip()
                    platform = platform_info.split('(')[0].strip()
                    if '热度' in platform_info:
                        hot_value = platform_info.split('热度')[1].strip(')').strip()
            elif '**时效：**' in line:
                break

        # 提取标题
        title_start = False
        titles = []
        title_types = []

        for i, line in enumerate(lines):
            if '### 🎯 推荐标题' in line:
                title_start = True
                continue
            elif title_start and line.startswith('### '):
                break
            elif title_start and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                title_content = line.split('.', 1)[1].strip()
                if '】' in title_content:
                    title_type = title_content.split('】')[0].replace('【', '').strip()
                    title_text = title_content.split('】')[1].strip()
                else:
                    title_type = '默认'
                    title_text = title_content

                title_types.append(title_type)
                titles.append(title_text)

        # 提取正文
        content_start = False
        content_lines = []
        for line in lines:
            if '### 📄 正文内容' in line:
                content_start = True
                continue
            elif content_start:
                if line.startswith('---') or line.startswith('##'):
                    break
                content_lines.append(line)

        post_content = '\n'.join(content_lines).strip()

        # 生成图片和视频建议
        image_suggestions = [
            "孩子使用平板/电脑学习的照片（真实场景）",
            "教育相关的图片（学校、书本、黑板等）",
            "添加醒目文字：'AI改变教育'、'美国学校'等"
        ]

        video_suggestions = [
            "录制孩子使用AI工具学习的真实场景（15-30秒）",
            "对比视频：传统学习 VS AI辅助学习的效果"
        ]

        # 为每个标题创建一条记录
        for title_type, title in zip(title_types, titles):
            posts.append({
                'original_topic': original_topic or post_title,
                'platform': platform or 'Hacker News',
                'category': 'AI教育',
                'title_type': title_type,
                'title': title,
                'content': post_content,
                'image_suggestions': ' | '.join(image_suggestions),
                'video_suggestions': ' | '.join(video_suggestions),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    return posts


def main():
    """主函数"""
    print("="*70)
    print("🔄 转换小红书爆文为CSV格式")
    print("="*70)
    print()

    # 查找小红书爆文文件
    import glob
    md_files = glob.glob('小红书爆文*.md')

    if not md_files:
        print("❌ 未找到小红书爆文文件")
        return

    print(f"📂 找到 {len(md_files)} 个文件:")
    for f in md_files:
        print(f"   - {f}")

    # 选择最新的文件
    latest_file = max(md_files, key=os.path.getmtime)
    print(f"\n📄 处理文件: {latest_file}\n")

    # 解析文件
    print("[*] 正在解析文件...")
    posts = parse_xiaohongshu_md(latest_file)
    print(f"✓ 解析到 {len(posts)} 条爆文数据\n")

    # 导出到CSV
    print("[*] 正在导出CSV...")
    csv_exporter = CSVExporter()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = csv_exporter.export_xiaohongshu_posts(posts, f'xiaohongshu_posts_{timestamp}.csv')

    print()
    print("="*70)
    print("✅ 转换完成！")
    print(f"CSV文件: {csv_file}")
    print("="*70)
    print()
    print("💡 提示:")
    print("- CSV文件可用Excel打开")
    print("- 包含列: 序号、原热点话题、来源平台、话题分类、标题类型、推荐标题、正文内容、建议配图、建议视频、生成时间")


if __name__ == '__main__':
    main()
