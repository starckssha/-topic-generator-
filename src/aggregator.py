"""
话题聚合器
"""
from typing import List, Dict, Tuple
from datetime import datetime
from collections import Counter


class TopicAggregator:
    """话题聚合器，用于整合多个平台的热点话题"""

    def __init__(self):
        self.all_topics = []
        self.platform_stats = {}

    def add_topics(self, topics: List[Dict], platform: str):
        """
        添加一个平台的话题

        Args:
            topics: 话题列表
            platform: 平台名称
        """
        self.all_topics.extend(topics)
        self.platform_stats[platform] = len(topics)

    def get_cross_platform_topics(self, min_platforms: int = 2) -> List[Tuple[str, List[str]]]:
        """
        找出在多个平台都出现的话题

        Args:
            min_platforms: 至少在多少个平台出现

        Returns:
            (话题标题, 出现的平台列表)的列表
        """
        # 按标题统计话题在各平台的出现情况
        topic_platforms = {}

        for topic in self.all_topics:
            title = topic.get('title', '').strip()
            platform = topic.get('platform', '')

            if title not in topic_platforms:
                topic_platforms[title] = set()
            topic_platforms[title].add(platform)

        # 筛选出在多个平台都出现的话题
        cross_platform = [
            (title, list(platforms))
            for title, platforms in topic_platforms.items()
            if len(platforms) >= min_platforms
        ]

        # 按出现平台数量排序
        cross_platform.sort(key=lambda x: len(x[1]), reverse=True)

        return cross_platform

    def get_hot_topics_by_platform(self) -> Dict[str, List[Dict]]:
        """
        按平台分组获取热点话题

        Returns:
            按平台分组的话题字典
        """
        platform_topics = {}

        for topic in self.all_topics:
            platform = topic.get('platform', '未知')
            if platform not in platform_topics:
                platform_topics[platform] = []
            platform_topics[platform].append(topic)

        # 按热度值排序每个平台的话题
        for platform in platform_topics:
            platform_topics[platform].sort(
                key=lambda x: x.get('hot_value', 0), reverse=True
            )

        return platform_topics

    def get_summary(self) -> Dict:
        """
        获取聚合统计摘要

        Returns:
            统计信息字典
        """
        return {
            'total_topics': len(self.all_topics),
            'platform_count': len(self.platform_stats),
            'platform_stats': self.platform_stats,
            'cross_platform_count': len(self.get_cross_platform_topics())
        }
