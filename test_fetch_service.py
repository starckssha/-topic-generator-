"""
测试FetchService
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.fetch_service import FetchService

def test_fetch():
    """测试抓取服务"""
    service = FetchService()

    print("=" * 70)
    print("测试热点抓取服务")
    print("=" * 70)

    result = service.fetch_hot_topics(
        platforms=['hackernews'],
        async_execution=False
    )

    print("\n抓取结果:")
    print(f"批次ID: {result.get('batch_id')}")
    print(f"状态: {result.get('status')}")
    print(f"总话题数: {result.get('total')}")
    print(f"成功平台数: {result.get('success_count')}")
    print(f"失败平台数: {result.get('failed_count')}")

    # 获取结果
    batch_id = result.get('batch_id')
    if batch_id:
        topics = service.get_fetch_results(batch_id)
        print(f"\n从数据库获取到 {len(topics)} 条话题")
        if topics:
            print(f"第一条话题: {topics[0].title}")

if __name__ == '__main__':
    test_fetch()
