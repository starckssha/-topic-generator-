#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Generator - 网络热点话题聚合工具 (优化版 v2)

主程序入口 - 支持科技/教育分类
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

from src.fetchers import (
    WeiboFetcher,
    ZhihuFetcher,
    ToutiaoFetcher,
    BaiduFetcher,
    BilibiliFetcher,
    YouTubeFetcher,
    YouTubeAPIFetcher,
    TwitterFetcher,
    HackerNewsFetcher
)
from src.aggregator import TopicAggregator
from src.exporter import MarkdownExporter
from src.exporter_csv import CSVExporter
from config import CONFIG


# Fetcher工厂函数
def create_fetcher(platform: str):
    """根据平台名称创建对应的fetcher实例"""
    if platform == 'weibo':
        return WeiboFetcher()
    elif platform == 'zhihu':
        return ZhihuFetcher()
    elif platform == 'toutiao':
        return ToutiaoFetcher()
    elif platform == 'baidu':
        return BaiduFetcher()
    elif platform == 'bilibili':
        return BilibiliFetcher()
    elif platform == 'youtube_tech':
        return YouTubeFetcher(category='tech')
    elif platform == 'youtube_edu':
        return YouTubeFetcher(category='education')
    elif platform == 'youtube_tech_api':
        return YouTubeAPIFetcher(category='tech')
    elif platform == 'youtube_edu_api':
        return YouTubeAPIFetcher(category='education')
    elif platform == 'twitter_tech':
        return TwitterFetcher(category='tech')
    elif platform == 'twitter_edu':
        return TwitterFetcher(category='education')
    elif platform == 'hackernews':
        return HackerNewsFetcher()
    else:
        raise ValueError(f"不支持的平台: {platform}")


def main():
    """主函数"""
    print("=" * 70)
    print("Topic Generator v2 - 网络热点话题聚合工具")
    print("专注于科技和教育领域的话题聚合")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 创建输出目录
    output_dir = CONFIG.get('output_dir', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # 初始化抓取器、聚合器和导出器
    aggregator = TopicAggregator()
    exporter = MarkdownExporter()
    csv_exporter = CSVExporter()

    # 获取启用的平台
    enabled_platforms = CONFIG.get('enabled_platforms', ['hackernews'])
    
    # 统计
    success_count = 0
    total_count = len(enabled_platforms)

    print(f"配置的平台数量: {total_count}")
    print(f"启用的平台: {', '.join(enabled_platforms)}")
    print()

    # 遍历启用的平台
    for platform in enabled_platforms:
        try:
            # 获取话题数量配置
            platform_base = platform.replace('_tech', '').replace('_edu', '')
            count = CONFIG.get(f'{platform_base}_count', 20)
            if platform in ['youtube_tech', 'youtube_edu']:
                count = CONFIG.get('youtube_count', 20)
            elif platform in ['twitter_tech', 'twitter_edu']:
                count = CONFIG.get('twitter_count', 20)
            
            print(f"[*] 正在获取 {platform} 数据...")
            fetcher = create_fetcher(platform)
            topics = fetcher.fetch(count)
            
            if topics:
                platform_name = topics[0].get('platform', platform)
                aggregator.add_topics(topics, platform_name)
                success_count += 1
            print()
        except Exception as e:
            print(f"[!] 获取 {platform} 数据失败: {e}\n")

    # 获取聚合数据
    print("[*] 正在聚合数据...")
    platform_topics = aggregator.get_hot_topics_by_platform()
    cross_platform = aggregator.get_cross_platform_topics(min_platforms=2)
    summary = aggregator.get_summary()
    
    print(f"成功获取 {summary['total_topics']} 条话题")
    print(f"成功率: {success_count}/{total_count} ({success_count*100//total_count if total_count > 0 else 0}%)")
    if cross_platform:
        print(f"发现 {summary['cross_platform_count']} 个跨平台热点")
    print()

    # 导出Markdown报告
    print("[*] 正在生成Markdown报告...")
    output_file = exporter.export(
        platform_topics=platform_topics,
        cross_platform=cross_platform,
        summary=summary
    )

    # 导出CSV报告
    print("[*] 正在生成CSV报告...")
    # 收集所有话题
    all_topics = []
    for platform, topics in platform_topics.items():
        all_topics.extend(topics)

    csv_file = csv_exporter.export_topics(all_topics)

    # 生成汇总CSV
    csv_summary = csv_exporter.export_summary(all_topics)

    print()
    print("=" * 70)
    print("[+] 任务完成!")
    print(f"Markdown报告: {output_file}")
    print(f"CSV数据文件: {csv_file}")
    print(f"CSV汇总文件: {csv_summary}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    print("💡 提示:")
    print("- CSV文件可用Excel打开，方便查看和编辑")
    print("- 可使用Excel的筛选、排序功能分析数据")
    
    # 显示科技/教育话题统计
    tech_count = sum(1 for topics in platform_topics.values() 
                    for t in topics if t.get('category') in ['tech', 'education'])
    if tech_count > 0:
        print(f"\n[*] 科技/教育类话题: {tech_count} 条")


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
