"""
Reddit热点抓取器 - 科技/教育话题
"""
from typing import List, Dict
import requests
from ..base_fetcher import BaseFetcher


class RedditFetcher(BaseFetcher):
    """Reddit热点话题抓取器（科技/教育）"""

    def __init__(self, subreddit: str = 'technology'):
        """
        初始化Reddit抓取器

        Args:
            subreddit: 子版块名称
                - 'technology': 科技新闻
                - 'programming': 编程
                - 'MachineLearning': 机器学习
                - 'artificial': 人工智能
                - 'education': 教育
                - 'science': 科学
                - 'gadgets': 科技产品
        """
        super().__init__()
        self.subreddit = subreddit

    def fetch(self, count: int = 50) -> List[Dict]:
        """
        获取Reddit热门话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []

        try:
            print(f"尝试获取Reddit r/{self.subreddit} 热门话题...")

            # Reddit公开JSON API（无需认证）
            url = f"https://www.reddit.com/r/{self.subreddit}/hot.json?limit={count}"

            # 设置更真实的headers
            headers = self.session.headers.copy()
            headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            })

            response = self.session.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and 'children' in data['data']:
                    posts = data['data']['children']

                    for idx, post in enumerate(posts[:count], 1):
                        post_data = post['data']

                        title = post_data.get('title', '')
                        url = post_data.get('url', '')
                        permalink = f"https://www.reddit.com{post_data.get('permalink', '')}"
                        score = post_data.get('score', 0)  # 点赞数
                        num_comments = post_data.get('num_comments', 0)  # 评论数

                        if title:
                            topics.append({
                                'rank': idx,
                                'title': title,
                                'url': permalink,
                                'hot_value': score,  # 使用点赞数作为热度值
                                'platform': f'Reddit(r/{self.subreddit})',
                                'category': self._determine_category(title)
                            })

                    print(f"成功获取Reddit r/{self.subreddit}热门 {len(topics)} 条")
                    return topics
            else:
                print(f"Reddit API返回错误: {response.status_code}")

        except Exception as e:
            print(f"获取Reddit r/{self.subreddit}失败: {e}")

        return topics

    def _determine_category(self, title: str) -> str:
        """根据标题确定分类"""
        title_lower = title.lower()

        # 教育关键词
        edu_keywords = ['education', 'learning', 'school', 'university', 'student', 'teacher', 'course', 'tutorial', 'study', '教育', '学习', '大学']
        # AI关键词
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural', 'gpt', 'chatgpt', 'llm', 'model']

        if any(kw in title_lower for kw in edu_keywords):
            return 'education'
        elif any(kw in title_lower for kw in ai_keywords):
            return 'tech'
        else:
            return 'general'
