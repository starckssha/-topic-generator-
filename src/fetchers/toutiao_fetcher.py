"""
今日头条热点抓取器 - 优化版
"""
from typing import List, Dict
from ..base_fetcher import BaseFetcher


class ToutiaoFetcher(BaseFetcher):
    """今日头条热点话题抓取器"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取今日头条热点话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"

        try:
            data = self._get_json(url, referer='https://www.toutiao.com')
            if not data:
                return topics

            event_list = data.get('data', [])

            for idx, item in enumerate(event_list[:count], 1):
                title = item.get('Title', '')
                hot_value = item.get('HotValue', 0)

                topics.append({
                    'rank': idx,
                    'title': title,
                    'url': item.get('Url', ''),
                    'hot_value': hot_value,
                    'platform': '今日头条'
                })

            print(f"成功获取今日头条热点 {len(topics)} 条")
            return topics

        except Exception as e:
            print(f"获取今日头条热点时出错: {e}")
            return topics
