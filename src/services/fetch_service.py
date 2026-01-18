"""
热点抓取服务
将现有的抓取逻辑改造为服务类，集成到数据库
"""
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
import threading

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 设置标准输出编码为UTF-8（在添加路径之后）
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass  # 如果已经设置过则忽略

from src.fetchers import (
    WeiboFetcher,
    ZhihuFetcher,
    ToutiaoFetcher,
    BaiduFetcher,
    BilibiliFetcher,
    YouTubeFetcher,
    YouTubeAPIFetcher,
    TwitterFetcher,
    HackerNewsFetcher,
    RedditFetcher
)
from src.aggregator import TopicAggregator
from src.database.models import HotTopic, TaskExecution
from src.database.repositories import HotTopicRepository, TaskExecutionRepository
from config import CONFIG


class FetchProgress:
    """抓取进度数据类"""

    def __init__(self):
        self.total_platforms = 0
        self.completed_platforms = 0
        self.current_platform = ""
        self.results = {}
        self.status = "pending"  # pending, running, success, failed
        self.error_message = None

    def to_dict(self):
        return {
            'total_platforms': self.total_platforms,
            'completed_platforms': self.completed_platforms,
            'progress': (self.completed_platforms / self.total_platforms * 100) if self.total_platforms > 0 else 0,
            'current_platform': self.current_platform,
            'results': self.results,
            'status': self.status,
            'error_message': self.error_message
        }


class FetchService:
    """热点抓取服务类"""

    def __init__(self):
        self.aggregator = TopicAggregator()
        self.progress_store = {}  # 存储各任务的进度信息
        self.lock = threading.Lock()

    @staticmethod
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
        elif platform == 'reddit_tech':
            return RedditFetcher(subreddit='technology')
        elif platform == 'reddit_programming':
            return RedditFetcher(subreddit='programming')
        elif platform == 'reddit_ai':
            return RedditFetcher(subreddit='artificial')
        else:
            raise ValueError(f"不支持的平台: {platform}")

    def fetch_hot_topics(
        self,
        platforms: Optional[List[str]] = None,
        async_execution: bool = False
    ) -> Dict:
        """
        执行抓取任务

        Args:
            platforms: 指定平台列表，None则使用配置中的全部平台
            async_execution: 是否异步执行

        Returns:
            {
                'batch_id': '批次ID',
                'total': 100,
                'success_count': 8,
                'failed_count': 2,
                'platforms': {...}
            }
        """
        # 生成批次ID
        batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 初始化进度
        progress = FetchProgress()
        self.progress_store[batch_id] = progress

        if async_execution:
            # 异步执行
            thread = threading.Thread(
                target=self._fetch_worker,
                args=(batch_id, platforms, progress)
            )
            thread.start()
            return {
                'batch_id': batch_id,
                'status': 'running',
                'message': '抓取任务已启动（异步执行）'
            }
        else:
            # 同步执行
            return self._fetch_worker(batch_id, platforms, progress)

    def _fetch_worker(
        self,
        batch_id: str,
        platforms: Optional[List[str]],
        progress: FetchProgress
    ) -> Dict:
        """
        抓取工作线程

        Args:
            batch_id: 批次ID
            platforms: 平台列表
            progress: 进度对象

        Returns:
            执行结果
        """
        start_time = datetime.now()

        # 创建任务记录
        task = TaskExecution(
            task_type='fetch_hot_topics',
            batch_id=batch_id,
            status='running',
            start_time=start_time,
            triggered_by='manual'
        )
        task_id = TaskExecutionRepository.insert(task)

        # 获取平台列表
        if platforms is None:
            platforms = CONFIG.get('enabled_platforms', ['hackernews'])

        progress.total_platforms = len(platforms)
        progress.status = "running"

        success_count = 0
        failed_count = 0

        print(f"🚀 开始抓取热点话题（批次: {batch_id}）")
        print(f"配置的平台数量: {len(platforms)}")
        print(f"启用的平台: {', '.join(platforms)}")

        # 遍历平台抓取
        for platform in platforms:
            progress.current_platform = platform
            try:
                # 获取话题数量配置
                platform_base = platform.replace('_tech', '').replace('_edu', '')
                count = CONFIG.get(f'{platform_base}_count', 20)
                if platform in ['youtube_tech', 'youtube_edu']:
                    count = CONFIG.get('youtube_count', 20)
                elif platform in ['twitter_tech', 'twitter_edu']:
                    count = CONFIG.get('twitter_count', 20)

                print(f"[*] 正在获取 {platform} 数据...")
                fetcher = self.create_fetcher(platform)
                topics = fetcher.fetch(count)

                if topics:
                    platform_name = topics[0].get('platform', platform)
                    self.aggregator.add_topics(topics, platform_name)

                    # 转换为HotTopic模型并保存到数据库
                    hot_topics = []
                    for topic in topics:
                        hot_topic = HotTopic(
                            title=topic.get('title', ''),
                            platform=topic.get('platform', platform),
                            rank=topic.get('rank', 0),
                            hot_value=topic.get('hot_value', 0),
                            url=topic.get('url', ''),
                            category=topic.get('category', 'general'),
                            fetched_at=start_time,
                            batch_id=batch_id
                        )
                        hot_topics.append(hot_topic)

                    # 批量插入数据库
                    HotTopicRepository.batch_insert(hot_topics)

                    success_count += 1
                    progress.results[platform] = {
                        'status': 'success',
                        'count': len(topics)
                    }
                else:
                    failed_count += 1
                    progress.results[platform] = {
                        'status': 'failed',
                        'count': 0,
                        'error': 'No topics returned'
                    }

                progress.completed_platforms += 1
                print()

            except Exception as e:
                print(f"[!] 获取 {platform} 数据失败: {e}\n")
                failed_count += 1
                progress.results[platform] = {
                    'status': 'failed',
                    'count': 0,
                    'error': str(e)
                }
                progress.completed_platforms += 1

        # 聚合数据
        platform_topics = self.aggregator.get_hot_topics_by_platform()
        cross_platform = self.aggregator.get_cross_platform_topics(min_platforms=2)
        summary = self.aggregator.get_summary()

        print(f"[*] 数据聚合完成")
        print(f"成功获取 {summary['total_topics']} 条话题")
        print(f"成功率: {success_count}/{len(platforms)} ({success_count*100//len(platforms) if len(platforms) > 0 else 0}%)")
        if cross_platform:
            print(f"发现 {summary['cross_platform_count']} 个跨平台热点")

        # 更新任务记录
        end_time = datetime.now()
        duration_seconds = int((end_time - start_time).total_seconds())

        task_result = {
            'total': summary['total_topics'],
            'success_count': success_count,
            'failed_count': failed_count,
            'platforms': progress.results,
            'cross_platform_count': summary['cross_platform_count']
        }
        task.set_result_summary(task_result)

        TaskExecutionRepository.update_status(
            task_id,
            'success',
            end_time=end_time,
            duration_seconds=duration_seconds
        )

        progress.status = "success"

        return {
            'batch_id': batch_id,
            'status': 'success',
            'total': summary['total_topics'],
            'success_count': success_count,
            'failed_count': failed_count,
            'platforms': progress.results,
            'cross_platform_count': summary['cross_platform_count'],
            'duration_seconds': duration_seconds
        }

    def get_progress(self, batch_id: str) -> Optional[Dict]:
        """
        获取抓取进度

        Args:
            batch_id: 批次ID

        Returns:
            进度信息字典
        """
        progress = self.progress_store.get(batch_id)
        if progress:
            return progress.to_dict()
        return None

    def get_fetch_results(self, batch_id: str, limit: int = None) -> List[HotTopic]:
        """
        获取抓取结果

        Args:
            batch_id: 批次ID
            limit: 限制数量

        Returns:
            HotTopic实例列表
        """
        return HotTopicRepository.get_by_batch_id(batch_id, limit)


# 测试代码
if __name__ == '__main__':
    service = FetchService()

    # 测试抓取
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
