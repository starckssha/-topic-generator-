"""
YouTube热门抓取器 - 使用YouTube Data API v3
"""
from typing import List, Dict
import os
import sys
from ..base_fetcher import BaseFetcher

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import CONFIG


class YouTubeAPIFetcher(BaseFetcher):
    """YouTube热门话题抓取器（使用官方API）"""

    def __init__(self, category: str = 'tech', api_key: str = None):
        """
        初始化YouTube抓取器

        Args:
            category: 类别 'tech'(科技) 或 'education'(教育)
            api_key: YouTube Data API密钥（可选，默认从环境变量或配置文件获取）
        """
        super().__init__()
        self.category = category
        # 优先使用传入的api_key，其次环境变量，最后配置文件
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY') or CONFIG.get('youtube_api_key')

        if not self.api_key:
            print("[WARNING] 未找到YouTube API密钥，将使用HTML解析方式")
            print("[INFO] 请设置环境变量 YOUTUBE_API_KEY 或在config.py中配置")

        # YouTube视频分类ID
        # https://developers.google.com/youtube/v3/docs/videoCategories/list
        self.category_ids = {
            'tech': 28,      # Science & Technology
            'education': 27, # Education
            'science': 28,   # Science & Technology
            'howto': 26,     # HowTo & Style
            'gaming': 20,    # Gaming
            'music': 10,     # Music
            'news': 25,      # News & Politics
        }

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取YouTube热门视频

        Args:
            count: 获取的视频数量

        Returns:
            视频列表
        """
        # 如果没有API密钥，返回空列表
        if not self.api_key:
            print(f"YouTube {self.category} 需要API密钥")
            return []

        topics = []

        try:
            # 使用YouTube Data API v3获取热门视频
            category_id = self.category_ids.get(self.category, 28)

            # API端点：获取热门视频
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',  # 热门视频
                'regionCode': 'US',      # 美国地区
                'maxResults': min(count * 2, 50),  # 最多50个（API限制）
                'key': self.api_key
            }

            # 发送请求
            import json
            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                error_reason = error_data.get('error', {}).get('errors', [{}])[0].get('reason', 'Unknown')
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')

                if error_reason == 'quotaExceeded':
                    print(f"YouTube API配额已用完，请明天再试")
                elif error_reason == 'keyInvalid':
                    print(f"YouTube API密钥无效")
                else:
                    print(f"YouTube API错误: {error_msg}")

                return topics

            data = response.json()

            # 解析视频列表
            items = data.get('items', [])

            idx = 1
            for item in items:
                if idx > count:
                    break

                # 获取视频信息
                video_id = item.get('id', '')
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})

                title = snippet.get('title', '')
                description = snippet.get('description', '')

                # 获取观看数
                view_count = int(statistics.get('viewCount', 0))

                # 获取频道名称
                channel_title = snippet.get('channelTitle', '')

                # 过滤科技/教育相关内容
                if self._is_tech_or_education(title, description):
                    topics.append({
                        'rank': idx,
                        'title': title,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'hot_value': view_count,
                        'platform': f'YouTube({self.category})',
                        'category': self.category,
                        'channel': channel_title
                    })
                    idx += 1

            print(f"成功获取YouTube {self.category}热门 {len(topics)} 条")

        except Exception as e:
            print(f"获取YouTube热门时出错: {e}")

        return topics

    def fetch_by_category(self, category_id: int, count: int = 20) -> List[Dict]:
        """
        按指定分类获取热门视频

        Args:
            category_id: YouTube分类ID
            count: 获取的视频数量

        Returns:
            视频列表
        """
        if not self.api_key:
            return []

        topics = []

        try:
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',
                'regionCode': 'US',
                'videoCategoryId': category_id,
                'maxResults': min(count, 50),
                'key': self.api_key
            }

            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])

                for idx, item in enumerate(items[:count], 1):
                    video_id = item.get('id', '')
                    snippet = item.get('snippet', {})
                    statistics = item.get('statistics', {})

                    title = snippet.get('title', '')
                    view_count = int(statistics.get('viewCount', 0))

                    topics.append({
                        'rank': idx,
                        'title': title,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'hot_value': view_count,
                        'platform': f'YouTube(Category {category_id})'
                    })

        except Exception as e:
            print(f"按分类获取视频时出错: {e}")

        return topics

    def _is_tech_or_education(self, title: str, description: str = '') -> bool:
        """判断视频是否为科技或教育相关"""
        text = f"{title} {description}".lower()

        # 科技关键词
        tech_keywords = [
            'ai', 'artificial intelligence', 'tech', 'technology',
            'programming', 'code', 'coding', 'software', 'hardware',
            'gadget', 'review', 'iphone', 'android', 'mac', 'pc',
            'robot', 'space', 'nasa', 'quantum', 'crypto', 'blockchain',
            'machine learning', 'data', 'cyber', 'hack', 'security',
            '芯片', '人工智能', '科技', '编程', '代码', '软件', '硬件',
            '手机', '电脑', '机器人', '太空', '量子', '区块链',
            'gpt', 'chatgpt', 'llm', 'python', 'javascript', 'tutorial',
            'learn', 'course', 'explain', 'how to', 'science',
            'physics', 'chemistry', 'biology', 'math', 'study',
            'review', 'unbox', 'test', 'vs', 'comparison',
            'tutorial', 'guide', 'tips', 'tricks', 'setup'
        ]

        return any(keyword in text for keyword in tech_keywords)
