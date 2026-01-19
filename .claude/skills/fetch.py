#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点抓取Skill
从多个平台抓取热点话题并保存到数据库
"""
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.services import FetchService
from src.database.repositories import TaskExecutionRepository, HotTopicRepository


def main():
    """执行热点抓取"""
    print("=" * 70)
    print("🔥 热点抓取任务")
    print("=" * 70)
    print()

    # 创建抓取服务
    service = FetchService()

    # 同步执行抓取（可以观看进度）
    print("开始抓取热点话题...")
    print()

    result = service.fetch_hot_topics(
        platforms=None,  # 使用config.py中配置的平台
        async_execution=False  # 同步执行，可以看到实时日志
    )

    print()
    print("=" * 70)
    print("📊 抓取结果")
    print("=" * 70)
    print(f"批次ID: {result.get('batch_id')}")
    print(f"状态: {result.get('status')}")
    print(f"总话题数: {result.get('total', 0)}")
    print(f"成功平台: {result.get('success_count', 0)}/{result.get('total', 0)}")
    print(f"失败平台: {result.get('failed_count', 0)}")

    if 'cross_platform_count' in result:
        print(f"跨平台热点: {result['cross_platform_count']}")

    print()
    print("各平台详情:")
    platforms = result.get('platforms', {})
    for platform, info in platforms.items():
        status_icon = "✅" if info.get('status') == 'success' else "❌"
        print(f"  {status_icon} {platform}: {info.get('count', 0)} 条")
        if info.get('error'):
            print(f"      错误: {info['error']}")

    print()
    print("=" * 70)

    # 显示最新抓取的话题
    batch_id = result.get('batch_id')
    if batch_id and result.get('status') == 'success':
        print(f"📋 最新话题 (批次: {batch_id})")
        print("-" * 70)

        topics = HotTopicRepository.get_by_batch_id(batch_id, limit=10)
        for i, topic in enumerate(topics, 1):
            print(f"{i}. [{topic.platform}] {topic.title[:60]}...")
            print(f"   热值: {topic.hot_value} | 抓取时间: {topic.fetched_at}")

        if len(topics) >= 10:
            print(f"... (共 {len(topics)} 条)")
            print()
            print(f"💡 查看所有话题: {batch_id}")

    print()
    print("✅ 抓取完成!")
    print()

    return result


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
