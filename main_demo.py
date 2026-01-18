#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Generator - 演示版本（使用模拟数据）

展示科技/教育话题聚合功能
"""
import os
import sys
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.aggregator import TopicAggregator
from src.exporter import MarkdownExporter


def get_demo_topics():
    """获取演示用的科技/教育话题数据"""
    
    # Hacker News 模拟数据
    hackernews_topics = [
        {
            'rank': 1,
            'title': 'OpenAI o1模型正式发布，推理能力大幅提升',
            'url': 'https://openai.com/blog/o1',
            'hot_value': 856,
            'platform': 'Hacker News',
            'category': 'tech'
        },
        {
            'rank': 2,
            'title': 'Rust语言超越Python成为最受欢迎的编程语言',
            'url': 'https://news.ycombinator.com/item?id=12345',
            'hot_value': 742,
            'platform': 'Hacker News',
            'category': 'tech'
        },
        {
            'rank': 3,
            'title': '量子计算突破：IBM发布新型量子处理器',
            'url': 'https://research.ibm.com/quantum',
            'hot_value': 623,
            'platform': 'Hacker News',
            'category': 'tech'
        },
        {
            'rank': 4,
            'title': '教育科技：AI助教如何改变在线学习',
            'url': 'https://edtech.org/ai-tutors',
            'hot_value': 512,
            'platform': 'Hacker News',
            'category': 'education'
        },
        {
            'rank': 5,
            'title': '开源LLaMA 3模型性能评估报告',
            'url': 'https://arxiv.org/llama3',
            'hot_value': 489,
            'platform': 'Hacker News',
            'category': 'tech'
        },
        {
            'rank': 6,
            'title': 'WebAssembly 2.0规范发布',
            'url': 'https://webassembly.org',
            'hot_value': 421,
            'platform': 'Hacker News',
            'category': 'tech'
        },
        {
            'rank': 7,
            'title': '斯坦福大学免费发布机器学习课程',
            'url': 'https://stanford.edu/ml-course',
            'hot_value': 398,
            'platform': 'Hacker News',
            'category': 'education'
        },
        {
            'rank': 8,
            'title': 'Linux内核6.8发布：性能优化和安全改进',
            'url': 'https://kernel.org',
            'hot_value': 356,
            'platform': 'Hacker News',
            'category': 'tech'
        },
    ]
    
    # 今日头条科技话题（模拟）
    toutiao_topics = [
        {
            'rank': 1,
            'title': '雷军晒超强钢发明专利证书',
            'url': 'https://www.toutiao.com/article/123',
            'hot_value': 5242000,
            'platform': '今日头条(科技/教育)',
            'category': 'tech'
        },
        {
            'rank': 2,
            'title': '华为Mate70系列搭载全新芯片',
            'url': 'https://www.toutiao.com/article/456',
            'hot_value': 4890000,
            'platform': '今日头条(科技/教育)',
            'category': 'tech'
        },
        {
            'rank': 3,
            'title': 'AI大模型助力教育公平',
            'url': 'https://www.toutiao.com/article/789',
            'hot_value': 3200000,
            'platform': '今日头条(科技/教育)',
            'category': 'education'
        },
        {
            'rank': 4,
            'title': '新能源汽车销量创新高',
            'url': 'https://www.toutiao.com/article/101',
            'hot_value': 2850000,
            'platform': '今日头条(科技/教育)',
            'category': 'tech'
        },
    ]
    
    # B站科技话题（模拟）
    bilibili_topics = [
        {
            'rank': 1,
            'title': '【教程】零基础学习Python编程',
            'url': 'https://www.bilibili.com/video/123',
            'hot_value': 125000,
            'platform': 'B站',
            'category': 'education'
        },
        {
            'rank': 2,
            'title': '深度解析：ChatGPT原理与应用',
            'url': 'https://www.bilibili.com/video/456',
            'hot_value': 98000,
            'platform': 'B站',
            'category': 'tech'
        },
        {
            'rank': 3,
            'title': '2024年最新科技趋势分析',
            'url': 'https://www.bilibili.com/video/789',
            'hot_value': 76000,
            'platform': 'B站',
            'category': 'tech'
        },
    ]
    
    return {
        'Hacker News': hackernews_topics,
        '今日头条(科技/教育)': toutiao_topics,
        'B站': bilibili_topics,
    }


def main():
    """主函数"""
    print("=" * 70)
    print("Topic Generator - 科技/教育话题聚合工具 (演示版)")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n[*] 使用模拟数据展示功能\n")
    
    # 创建输出目录
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化聚合器和导出器
    aggregator = TopicAggregator()
    exporter = MarkdownExporter()
    
    # 获取演示数据
    all_demo_topics = get_demo_topics()
    
    total_count = 0
    tech_count = 0
    edu_count = 0
    
    # 添加演示数据
    for platform, topics in all_demo_topics.items():
        aggregator.add_topics(topics, platform)
        total_count += len(topics)
        
        for topic in topics:
            if topic.get('category') == 'tech':
                tech_count += 1
            elif topic.get('category') == 'education':
                edu_count += 1
        
        print(f"[+] {platform}: {len(topics)} 条话题")
    
    print(f"\n[*] 总计获取 {total_count} 条话题")
    print(f"    - 科技类: {tech_count} 条")
    print(f"    - 教育类: {edu_count} 条")
    print()
    
    # 获取聚合数据
    platform_topics = aggregator.get_hot_topics_by_platform()
    cross_platform = aggregator.get_cross_platform_topics(min_platforms=2)
    summary = aggregator.get_summary()
    
    # 导出Markdown报告
    print("[*] 正在生成Markdown报告...")
    output_file = exporter.export(
        platform_topics=platform_topics,
        cross_platform=cross_platform,
        summary=summary
    )
    
    print()
    print("=" * 70)
    print("[+] 演示完成！")
    print(f"报告已保存到: {output_file}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("[*] 提示：当网络问题解决后，使用以下命令获取真实数据：")
    print("    python main.py        # 使用主程序")
    print("    python main_tech.py   # 使用科技话题过滤")
    print("=" * 70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[!] 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
