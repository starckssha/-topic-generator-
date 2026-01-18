"""
Hacker News抓取器 - 科技新闻聚合
"""
from typing import List, Dict
from ..base_fetcher import BaseFetcher


class HackerNewsFetcher(BaseFetcher):
    """Hacker News热门话题抓取器（科技新闻）"""

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取Hacker News热门话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []
        
        # Hacker News官方API（无需认证）
        api_urls = [
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            'https://hacker-news.firebaseio.com/v0/newstories.json',
            'https://hacker-news.firebaseio.com/v0/beststories.json'
        ]
        
        for api_url in api_urls:
            try:
                print(f"尝试Hacker News API: {api_url.split('/')[-1]}...")
                
                # 获取故事ID列表
                story_ids = self._get_json(api_url)
                if not story_ids:
                    continue
                
                # 获取前N个故事的详细信息
                idx = 1
                for story_id in story_ids[:count * 2]:  # 多获取一些用于过滤
                    if idx > count:
                        break
                    
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story = self._get_json(story_url)
                    
                    if not story:
                        continue
                    
                    title = story.get('title', '')
                    if not title:
                        continue
                    
                    # 过滤科技相关
                    if not self._is_tech_related(title):
                        continue
                    
                    url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    score = story.get('score', 0)
                    
                    topics.append({
                        'rank': idx,
                        'title': title,
                        'url': url,
                        'hot_value': score,
                        'platform': 'Hacker News',
                        'category': 'tech'
                    })
                    idx += 1
                
                if topics:
                    print(f"成功获取Hacker News热门 {len(topics)} 条")
                    return topics
                
            except Exception as e:
                print(f"此API端点失败: {e}")
                continue
        
        print("Hacker News所有API端点均失败")
        return topics

    def _is_tech_related(self, title: str) -> bool:
        """判断标题是否为科技相关"""
        title_lower = title.lower()
        
        # Hacker News本身就是科技社区，大部分都是科技相关
        # 但我们可以过滤掉明显不相关的
        
        non_tech_keywords = [
            'politics', 'election', 'war', 'religion', 'sports',
            'celebrity', 'gossip', 'fashion', 'food'
        ]
        
        if any(keyword in title_lower for keyword in non_tech_keywords):
            return False
        
        return True
