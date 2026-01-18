"""
知乎热榜抓取器 - 优化版
"""
from typing import List, Dict
import re
from ..base_fetcher import BaseFetcher


class ZhihuFetcher(BaseFetcher):
    """知乎热榜话题抓取器"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取知乎热榜话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        
        # 尝试多个API端点
        apis = [
            {
                'url': 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50',
                'referer': 'https://www.zhihu.com/hot',
                'parser': self._parse_api_v1
            },
            {
                'url': 'https://m.zhihu.com/api/v4/questions/hot',
                'referer': 'https://m.zhihu.com',
                'parser': self._parse_api_v2
            }
        ]

        for api in apis:
            try:
                print(f"尝试知乎API: {api['url'][:50]}...")
                data = self._get_json(api['url'], referer=api['referer'])
                
                if data:
                    topics = api['parser'](data, count)
                    if topics:
                        print(f"成功获取知乎热榜 {len(topics)} 条")
                        return topics
            except Exception as e:
                print(f"此API端点失败: {e}")
                continue

        print("知乎热榜所有API端点均失败")
        return topics

    def _parse_api_v1(self, data: dict, count: int) -> List[Dict]:
        """解析桌面API格式"""
        topics = []
        if not data:
            return topics

        hot_list = data.get('data', [])
        for idx, item in enumerate(hot_list[:count], 1):
            target = item.get('target', {})
            title = target.get('title', '')
            question_id = target.get('id', '')

            # 提取热度值
            hot_value = 0
            detail_text = item.get('detail_text', '')
            if detail_text:
                match = re.search(r'[\d,]+', detail_text)
                if match:
                    hot_value = int(match.group().replace(',', ''))

            topics.append({
                'rank': idx,
                'title': title,
                'url': f"https://www.zhihu.com/question/{question_id}",
                'hot_value': hot_value,
                'excerpt': target.get('excerpt', ''),
                'platform': '知乎'
            })
        return topics

    def _parse_api_v2(self, data: dict, count: int) -> List[Dict]:
        """解析移动端API格式"""
        topics = []
        if not data:
            return topics

        hot_list = data.get('data', [])
        for idx, item in enumerate(hot_list[:count], 1):
            title = item.get('title', '')
            question_id = item.get('id', '')
            hot_value = item.get('hotness', 0) or 0

            topics.append({
                'rank': idx,
                'title': title,
                'url': f"https://www.zhihu.com/question/{question_id}",
                'hot_value': int(hot_value),
                'excerpt': item.get('excerpt', ''),
                'platform': '知乎'
            })
        return topics
