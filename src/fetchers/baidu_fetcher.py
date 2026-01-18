"""
百度热搜抓取器
"""
from typing import List, Dict
import re
from ..base_fetcher import BaseFetcher


class BaiduFetcher(BaseFetcher):
    """百度热搜话题抓取器"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取百度热搜话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        url = "https://top.baidu.com/api/board?platform=wise&show_type=realtime"

        try:
            data = self._get_json(url, referer='https://top.baidu.com/board')
            if not data:
                return topics

            cards = data.get('data', {}).get('cards', [])
            if not cards:
                return topics

            hot_list = cards[0].get('content', [])
            
            for idx, item in enumerate(hot_list[:count], 1):
                title = item.get('word', '')
                hot_value = 0
                
                # 尝试获取热度值
                hot_score = item.get('hotScore', 0)
                if hot_score:
                    hot_value = int(hot_score)

                topics.append({
                    'rank': idx,
                    'title': title,
                    'url': f"https://www.baidu.com/s?wd={title}",
                    'hot_value': hot_value,
                    'platform': '百度'
                })

            print(f"成功获取百度热搜 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"获取百度热搜时出错: {e}")
            return topics
