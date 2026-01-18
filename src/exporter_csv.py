# -*- coding: utf-8 -*-
"""
CSV导出器 - 支持Excel格式
"""

import csv
import os
from datetime import datetime
from typing import List, Dict


class CSVExporter:
    """导出热点数据为CSV格式，兼容Excel"""

    def __init__(self, output_dir: str = None):
        """
        初始化CSV导出器

        Args:
            output_dir: 输出目录，默认为./output
        """
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_topics(self, topics: List[Dict], filename: str = None) -> str:
        """
        导出热点话题到CSV文件

        Args:
            topics: 热点话题列表
            filename: 文件名（不含扩展名），默认为hot_topics_YYYYMMDD_HHMMSS

        Returns:
            导出文件的完整路径
        """
        if not topics:
            print("[CSV] 没有数据可导出")
            return None

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'hot_topics_{timestamp}.csv'

        filepath = os.path.join(self.output_dir, filename)

        # 定义CSV列
        fieldnames = [
            '平台',
            '排名',
            '标题',
            '链接',
            '热度',
            '分类',
            '时间戳'
        ]

        # 写入CSV文件（使用UTF-8 BOM编码以兼容Excel）
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for topic in topics:
                row = {
                    '平台': topic.get('platform', ''),
                    '排名': topic.get('rank', ''),
                    '标题': topic.get('title', ''),
                    '链接': topic.get('url', ''),
                    '热度': topic.get('hot_value', ''),
                    '分类': topic.get('category', ''),
                    '时间戳': topic.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }
                writer.writerow(row)

        print(f"[CSV] ✅ 已导出 {len(topics)} 条数据到: {filepath}")
        return filepath

    def export_xiaohongshu_posts(self, posts_data: List[Dict], filename: str = None) -> str:
        """
        导出小红书爆文到CSV文件

        Args:
            posts_data: 爆文数据列表，每条包含标题列表和正文
            filename: 文件名（不含扩展名）

        Returns:
            导出文件的完整路径
        """
        if not posts_data:
            print("[CSV] 没有爆文数据可导出")
            return None

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'xiaohongshu_posts_{timestamp}.csv'

        filepath = os.path.join(self.output_dir, filename)

        # 定义CSV列 - 按用户要求包含题目、内容、图片/视频建议
        fieldnames = [
            '序号',
            '原热点话题',
            '来源平台',
            '话题分类',
            '标题类型',
            '推荐标题',
            '正文内容',
            '建议配图',
            '建议视频',
            '生成时间'
        ]

        # 写入CSV文件
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for idx, post in enumerate(posts_data, start=1):
                row = {
                    '序号': idx,
                    '原热点话题': post.get('original_topic', ''),
                    '来源平台': post.get('platform', ''),
                    '话题分类': post.get('category', ''),
                    '标题类型': post.get('title_type', ''),
                    '推荐标题': post.get('title', ''),
                    '正文内容': post.get('content', ''),
                    '建议配图': post.get('image_suggestions', ''),
                    '建议视频': post.get('video_suggestions', ''),
                    '生成时间': post.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }
                writer.writerow(row)

        print(f"[CSV] ✅ 已导出 {len(posts_data)} 条爆文数据到: {filepath}")
        return filepath

    def export_summary(self, all_topics: List[Dict], filename: str = None) -> str:
        """
        导出热点数据汇总（按平台统计）

        Args:
            all_topics: 所有热点话题列表
            filename: 文件名（不含扩展名）

        Returns:
            导出文件的完整路径
        """
        if not all_topics:
            print("[CSV] 没有数据可导出")
            return None

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'hot_topics_summary_{timestamp}.csv'

        filepath = os.path.join(self.output_dir, filename)

        # 按平台统计
        platform_stats = {}
        for topic in all_topics:
            platform = topic.get('platform', '未知')
            if platform not in platform_stats:
                platform_stats[platform] = {
                    'count': 0,
                    'topics': []
                }
            platform_stats[platform]['count'] += 1
            platform_stats[platform]['topics'].append(topic.get('title', ''))

        # 定义CSV列
        fieldnames = [
            '平台',
            '话题数量',
            '话题列表'
        ]

        # 写入CSV文件
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for platform, stats in sorted(platform_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                row = {
                    '平台': platform,
                    '话题数量': stats['count'],
                    '话题列表': ' | '.join(stats['topics'][:10])  # 只显示前10个
                }
                writer.writerow(row)

        print(f"[CSV] ✅ 已导出汇总数据到: {filepath}")
        return filepath
