"""
测试GenerateService
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.generate_service import GenerateService
from src.database.repositories import HotTopicRepository

def test_generate():
    """测试生成服务"""
    service = GenerateService()

    print("=" * 70)
    print("测试爆文生成服务")
    print("=" * 70)

    # 获取最近的话题
    topics = HotTopicRepository.get_available_topics(days=1, limit=3)
    print(f"\n找到 {len(topics)} 个可用话题")

    if topics:
        print("话题列表:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic.title} (ID: {topic.id})")

        topic_ids = [t.id for t in topics[:2]]  # 只测试前2个
        print(f"\n开始生成爆文（使用前2个话题）...")

        result = service.generate_viral_posts(
            topic_ids=topic_ids,
            async_execution=False
        )

        print("\n生成结果:")
        print(f"批次ID: {result.get('batch_id')}")
        print(f"状态: {result.get('status')}")
        print(f"总话题数: {result.get('total')}")
        print(f"成功数: {result.get('success')}")
        print(f"失败数: {result.get('failed')}")
        print(f"生成爆文数: {result.get('total_posts')}")
        print(f"执行时长: {result.get('duration_seconds')}秒")

        # 获取生成的爆文
        batch_id = result.get('batch_id')
        if batch_id:
            posts = service.get_generated_posts(batch_id)
            print(f"\n从数据库获取到 {len(posts)} 篇爆文")
            if posts:
                print(f"\n第一篇爆文示例:")
                print(f"标题: {posts[0].recommended_title}")
                print(f"类型: {posts[0].title_type}")
                print(f"内容长度: {len(posts[0].content)} 字符")
    else:
        print("没有可用的话题，请先运行抓取服务")

if __name__ == '__main__':
    test_generate()
