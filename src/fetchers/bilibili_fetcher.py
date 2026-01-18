"""
B站热门抓取器
"""
from typing import List, Dict
from ..base_fetcher import BaseFetcher


class BilibiliFetcher(BaseFetcher):
    """B站热门话题抓取器"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取B站热门话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        url = "https://api.bilibili.com/x/web-interface/popular?ps=50"

        try:
            data = self._get_json(url, referer='https://www.bilibili.com')
            if not data or data.get('code') != 0:
                return topics

            video_list = data.get('data', {}).get('list', [])

            for idx, item in enumerate(video_list[:count], 1):
                title = item.get('title', '')
                aid = item.get('aid', '')
                hot_value = item.get('stat', {}).get('view', 0)

                topics.append({
                    'rank': idx,
                    'title': title,
                    'url': f"https://www.bilibili.com/video/av{aid}",
                    'hot_value': hot_value,
                    'platform': 'B站'
                })

            print(f"成功获取B站热门 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"获取B站热门时出错: {e}")
            return topics
