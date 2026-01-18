"""测试内容生成功能"""
import sys
import io

# 只在未包装时包装stdout
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.database.repositories import HotTopicRepository, ViralPostRepository
from src.services.generate_service import GenerateService
from collections import defaultdict

def test_generation():
    # 获取最新的Hacker News话题
    topics = HotTopicRepository.get_available_topics(days=1, limit=50)
    hn_topics = [t for t in topics if t.platform == 'Hacker News'][:2]

    print(f'选择 {len(hn_topics)} 个Hacker News话题进行测试\n')

    # 手动标记为教育/AI相关
    for topic in hn_topics:
        topic.category = 'AI变革'

    # 生成爆文
    topic_ids = [t.id for t in hn_topics]
    print('开始生成爆文（使用AI智能生成）...\n')

    service = GenerateService()
    result = service.generate_viral_posts(
        topic_ids=topic_ids,
        async_execution=False
    )

    print(f'\n生成结果:')
    print(f'状态: {result.get("status")}')
    print(f'生成爆文数: {result.get("total_posts")}')
    print(f'耗时: {result.get("duration_seconds")} 秒')

    # 检查内容差异性
    posts = ViralPostRepository.get_by_batch_id(result['batch_id'])
    print(f'\n检查内容差异性:')
    print('=' * 100)

    posts_by_topic = defaultdict(list)
    for post in posts:
        posts_by_topic[post.original_topic].append(post)

    for topic_title, topic_posts in list(posts_by_topic.items())[:1]:
        print(f'\n话题: {topic_title[:70]}...')
        print('-' * 100)

        for i, post in enumerate(topic_posts):
            print(f'\n[{i+1}] 标题类型: {post.title_type}')
            print(f'    推荐标题: {post.recommended_title}')
            content_lines = post.content.split('\n')[:5]
            content_preview = ' '.join(line.strip() for line in content_lines if line.strip())
            print(f'    内容预览: {content_preview[:150]}...')
            print(f'    内容长度: {len(post.content)} 字符')

if __name__ == '__main__':
    test_generation()
