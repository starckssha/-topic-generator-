#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
话题去重管理器 - 记录已使用的话题，避免重复生成
"""
import os
import json
from datetime import datetime
from typing import List, Set, Dict


class TopicTracker:
    """话题追踪器 - 管理已使用的话题"""

    def __init__(self, tracker_file='output/used_topics.json'):
        """
        初始化追踪器

        Args:
            tracker_file: 追踪文件路径
        """
        self.tracker_file = tracker_file
        self.used_topics: Dict[str, List[Dict]] = {}
        self._load_tracker()

    def _load_tracker(self):
        """从文件加载已使用的话题"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    self.used_topics = json.load(f)
            except Exception as e:
                print(f"⚠️ 加载话题追踪文件失败: {e}")
                self.used_topics = {}
        else:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
            self.used_topics = {}

    def _save_tracker(self):
        """保存已使用的话题到文件"""
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.used_topics, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存话题追踪文件失败: {e}")

    def is_topic_used(self, topic_title: str, days: int = 30) -> bool:
        """
        检查话题是否在指定天数内已使用

        Args:
            topic_title: 话题标题
            days: 检查天数（默认30天）

        Returns:
            True如果已使用，False如果未使用
        """
        # 标准化话题标题（去除空格、标点等）
        normalized_title = self._normalize_title(topic_title)

        # 检查是否在已使用列表中
        if normalized_title in self.used_topics:
            # 检查时间是否在指定天数内
            for record in self.used_topics[normalized_title]:
                used_date = datetime.fromisoformat(record['used_at'])
                days_diff = (datetime.now() - used_date).days

                if days_diff <= days:
                    return True

        return False

    def mark_topic_used(self, topic_title: str, metadata: Dict = None):
        """
        标记话题为已使用

        Args:
            topic_title: 话题标题
            metadata: 额外的元数据（平台、分类等）
        """
        normalized_title = self._normalize_title(topic_title)

        if normalized_title not in self.used_topics:
            self.used_topics[normalized_title] = []

        # 添加使用记录
        record = {
            'used_at': datetime.now().isoformat(),
            'original_title': topic_title,
            'metadata': metadata or {}
        }

        self.used_topics[normalized_title].append(record)
        self._save_tracker()

    def filter_unused_topics(self, topics: List[Dict], days: int = 30) -> List[Dict]:
        """
        过滤掉已使用的话题

        Args:
            topics: 话题列表
            days: 检查天数（默认30天）

        Returns:
            未使用的话题列表
        """
        unused = []
        for topic in topics:
            title = topic.get('title', '')
            if not self.is_topic_used(title, days):
                unused.append(topic)

        return unused

    def _normalize_title(self, title: str) -> str:
        """
        标准化标题用于比较

        Args:
            title: 原始标题

        Returns:
            标准化后的标题
        """
        # 转小写
        normalized = title.lower().strip()
        # 去除多余空格
        normalized = ' '.join(normalized.split())
        # 去除常见标点
        for char in ['!', '?', '.', ',', '。', '！', '？', '，', '、']:
            normalized = normalized.replace(char, '')

        return normalized

    def get_stats(self) -> Dict:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        total_unique = len(self.used_topics)
        total_records = sum(len(records) for records in self.used_topics.values())

        # 统计最近7天、30天使用的话题
        now = datetime.now()
        last_7_days = 0
        last_30_days = 0

        for records in self.used_topics.values():
            for record in records:
                used_date = datetime.fromisoformat(record['used_at'])
                days_diff = (now - used_date).days

                if days_diff <= 7:
                    last_7_days += 1
                if days_diff <= 30:
                    last_30_days += 1

        return {
            'total_unique_topics': total_unique,
            'total_usage_records': total_records,
            'used_last_7_days': last_7_days,
            'used_last_30_days': last_30_days
        }

    def print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()

        print("\n" + "="*70)
        print("📊 话题使用统计")
        print("="*70)
        print(f"累计使用话题数: {stats['total_unique_topics']}")
        print(f"总使用记录数: {stats['total_usage_records']}")
        print(f"最近7天使用: {stats['used_last_7_days']}")
        print(f"最近30天使用: {stats['used_last_30_days']}")
        print("="*70)


# 便捷函数
def get_tracker() -> TopicTracker:
    """获取话题追踪器实例"""
    return TopicTracker()


if __name__ == '__main__':
    # 测试代码
    tracker = get_tracker()

    # 测试检查
    test_topic = "AI在教育中的应用"
    is_used = tracker.is_topic_used(test_topic)
    print(f"话题 '{test_topic}' 是否已使用: {is_used}")

    # 测试标记
    tracker.mark_topic_used(test_topic, {'platform': 'hackernews', 'category': 'AI'})

    # 再次检查
    is_used = tracker.is_topic_used(test_topic)
    print(f"标记后，话题 '{test_topic}' 是否已使用: {is_used}")

    # 打印统计
    tracker.print_stats()
