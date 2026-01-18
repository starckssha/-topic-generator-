#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Generator - 科技/教育话题聚合工具

从通用平台获取话题后，过滤出科技和教育类别
"""
import os
import sys
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.fetchers import ToutiaoFetcher, BaiduFetcher, BilibiliFetcher
from src.aggregator import TopicAggregator
from src.exporter import MarkdownExporter
from config_tech import CONFIG


def is_tech_or_education(title: str, keywords_tech: list, keywords_edu: list) -> tuple:
    """
    判断话题是否为科技或教育相关
    
    Returns:
        (是否匹配, 类别)
    """
    title_lower = title.lower()
    
    # 检查科技关键词
    for keyword in keywords_tech:
        if keyword.lower() in title_lower:
            return (True, 'tech')
    
    # 检查教育关键词
    for keyword in keywords_edu:
        if keyword.lower() in title_lower:
            return (True, 'education')
    
    return (False, None)


def filter_topics(topics: list, config: dict) -> list:
    """过滤话题，只保留科技/教育相关"""
    tech_keywords = config.get('tech_keywords', [])
    edu_keywords = config.get('education_keywords', [])
    
    filtered = []
    for topic in topics:
        title = topic.get('title', '')
        is_match, category = is_tech_or_education(title, tech_keywords, edu_keywords)
        
        if is_match:
            topic['category'] = category
            filtered.append(topic)
    
    return filtered


def main():
    """主函数"""
    print("=" * 70)
    print("Topic Generator - 科技/教育话题聚合工具")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 创建输出目录
    output_dir = CONFIG.get('output_dir', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # 初始化聚合器和导出器
    aggregator = TopicAggregator()
    exporter = MarkdownExporter()

    enabled_platforms = CONFIG.get('enabled_platforms', ['toutiao'])
    should_filter = CONFIG.get('filter_by_category', True)
    
    print(f"启用的平台: {', '.join(enabled_platforms)}")
    print(f"话题过滤: {'启用' if should_filter else '禁用'}")
    print()

    total_raw = 0
    total_filtered = 0

    # 遍历启用的平台
    for platform in enabled_platforms:
        try:
            print(f"[*] 正在获取 {platform} 数据...")
            
            if platform == 'toutiao':
                fetcher = ToutiaoFetcher()
            elif platform == 'baidu':
                fetcher = BaiduFetcher()
            elif platform == 'bilibili':
                fetcher = BilibiliFetcher()
            else:
                print(f"不支持的平台: {platform}")
                continue
            
            count = CONFIG.get(f'{platform}_count', 50)
            topics = fetcher.fetch(count)
            total_raw += len(topics)
            
            if topics:
                # 过滤科技/教育话题
                if should_filter:
                    print(f"[*] 过滤科技/教育话题...")
                    filtered_topics = filter_topics(topics, CONFIG)
                    print(f"    原始: {len(topics)} 条 -> 过滤后: {len(filtered_topics)} 条")
                    
                    if filtered_topics:
                        platform_name = f"{platform}(科技/教育)"
                        aggregator.add_topics(filtered_topics, platform_name)
                        total_filtered += len(filtered_topics)
                else:
                    aggregator.add_topics(topics, platform)
                    total_filtered += len(topics)
            print()
            
        except Exception as e:
            print(f"[!] 获取 {platform} 数据失败: {e}\n")

    # 获取聚合数据
    print("[*] 正在聚合数据...")
    platform_topics = aggregator.get_hot_topics_by_platform()
    cross_platform = aggregator.get_cross_platform_topics(min_platforms=2)
    summary = aggregator.get_summary()
    
    print(f"\n统计:")
    print(f"  原始话题: {total_raw} 条")
    print(f"  科技/教育话题: {total_filtered} 条")
    print(f"  过滤率: {total_filtered*100//total_raw if total_raw > 0 else 0}%")
    print()

    # 导出Markdown报告
    print("[*] 正在生成Markdown报告...")
    output_file = exporter.export(
        platform_topics=platform_topics,
        cross_platform=cross_platform,
        summary=summary
    )

    print()
    print("=" * 70)
    print("[+] 任务完成!")
    print(f"报告已保存到: {output_file}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
