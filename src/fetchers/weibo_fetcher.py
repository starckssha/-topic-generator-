"""
微博热搜抓取器 - 优化版
"""
from typing import List, Dict
from ..base_fetcher import BaseFetcher


class WeiboFetcher(BaseFetcher):
    """微博热搜话题抓取器"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取微博热搜话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        
        # 尝试多个API端点
        apis = [
            {
                'url': 'https://weibo.com/ajax/side/hotSearch',
                'referer': 'https://weibo.com',
                'parser': self._parse_api_v1
            },
            {
                'url': 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot',
                'referer': 'https://m.weibo.cn',
                'parser': self._parse_api_v2
            }
        ]

        for api in apis:
            try:
                print(f"尝试微博API: {api['url'][:50]}...")
                data = self._get_json(api['url'], referer=api['referer'])
                
                if data:
                    topics = api['parser'](data, count)
                    if topics:
                        print(f"成功获取微博热搜 {len(topics)} 条")
                        return topics
            except Exception as e:
                print(f"此API端点失败: {e}")
                continue

        print("微博热搜所有API端点均失败")
        return topics

    def _parse_api_v1(self, data: dict, count: int) -> List[Dict]:
        """解析API v1格式"""
        topics = []
        if not data or data.get('ok') != 1:
            return topics

        realpos = data.get('data', {}).get('realpos', [])
        for idx, item in enumerate(realpos[:count], 1):
            topics.append({
                'rank': idx,
                'title': item.get('word', ''),
                'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                'hot_value': item.get('num', 0),
                'category': item.get('category', ''),
                'platform': '微博'
            })
        return topics

    def _parse_api_v2(self, data: dict, count: int) -> List[Dict]:
        """解析移动端API格式"""
        topics = []
        if not data:
            return topics

        cards = data.get('data', {}).get('cards', [])
        if not cards:
            return topics

        hot_board = cards[0].get('card_group', [])
        for idx, item in enumerate(hot_board[:count], 1):
            title = item.get('title_sub', '') or item.get('title', '')
            hot_value = 0
            
            # 尝试解析热度值
            desc = item.get('desc', '')
            if desc:
                import re
                match = re.search(r'(\d+)', desc)
                if match:
                    hot_value = int(match.group(1))

            topics.append({
                'rank': idx,
                'title': title,
                'url': item.get('scheme', ''),
                'hot_value': hot_value,
                'platform': '微博'
            })
        return topics
