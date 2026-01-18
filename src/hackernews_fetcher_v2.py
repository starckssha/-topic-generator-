"""
Hacker News抓取器 - 使用curl绕过SSL问题
"""
from typing import List, Dict
import subprocess
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class HackerNewsFetcherCurl:
    """使用curl获取数据，绕过Python SSL问题"""

    def __init__(self):
        self.proxy = "http://127.0.0.1:7897"
        self.timeout = 10

    def fetch(self, count: int = 20) -> List[Dict]:
        """使用curl获取Hacker News热门话题"""
        topics = []
        
        api_urls = [
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            'https://hacker-news.firebaseio.com/v0/newstories.json',
            'https://hacker-news.firebaseio.com/v0/beststories.json'
        ]
        
        for api_url in api_urls:
            try:
                print(f"[*] 尝试: {api_url.split('/')[-1]}")
                
                # 使用curl通过代理获取数据
                story_ids = self._curl_get_json(api_url)
                
                if not story_ids:
                    continue
                
                print(f"    获取到 {len(story_ids)} 个故事ID")
                
                # 获取前N个故事
                for idx, story_id in enumerate(story_ids[:count * 2], 1):
                    if idx > count:
                        break
                    
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story = self._curl_get_json(story_url)
                    
                    if not story:
                        continue
                    
                    title = story.get('title', '')
                    if not title:
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
                
                if topics:
                    print(f"✓ 成功获取 Hacker News {len(topics)} 条")
                    return topics
                
            except Exception as e:
                print(f"    失败: {e}")
                continue
        
        print("Hacker News 所有API端点均失败")
        return topics

    def _curl_get_json(self, url: str) -> dict:
        """使用curl获取JSON数据"""
        try:
            # 构建curl命令
            cmd = [
                'curl', '-s', '-k',  # silent, insecure
                '-x', self.proxy,    # 使用代理
                '--connect-timeout', str(self.timeout),
                '-H', 'Accept: application/json',
                url
            ]
            
            # 执行curl
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 5
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return None
                
        except subprocess.TimeoutExpired:
            print(f"    超时")
            return None
        except Exception as e:
            return None


# 测试
if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    
    print("=" * 60)
    print("测试 Hacker News (使用 curl)")
    print("=" * 60)
    print()
    
    fetcher = HackerNewsFetcherCurl()
    topics = fetcher.fetch(10)
    
    if topics:
        print()
        print(f"成功！获取到 {len(topics)} 条科技新闻：")
        print()
        for i, topic in enumerate(topics[:5], 1):
            print(f"{i}. {topic['title']}")
            print(f"   热度: {topic['hot_value']}")
            print()
    else:
        print("未能获取数据")
