"""
YouTube热门抓取器 - 科技/教育类别
"""
from typing import List, Dict
from ..base_fetcher import BaseFetcher


class YouTubeFetcher(BaseFetcher):
    """YouTube热门话题抓取器（科技/教育类别）"""

    def __init__(self, category: str = 'tech'):
        """
        初始化YouTube抓取器

        Args:
            category: 类别 'tech'(科技) 或 'education'(教育)
        """
        super().__init__()
        self.category = category

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取YouTube热门话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        # YouTube的categoryId: 1=Film, 2=Autos, 10=Music, 15=Pets, 17=Sports,
        # 20=Games, 22=People, 23=Comedy, 24=Entertainment, 25=News,
        # 26=HowTo, 27=Education, 28=Science & Technology

        category_map = {
            'tech': 28,      # Science & Technology
            'education': 27, # Education
            'science': 28,   # Science & Technology
            'howto': 26      # HowTo & Style
        }

        category_id = category_map.get(self.category, 28)

        topics = []

        try:
            # 尝试多种方式获取YouTube数据
            # 方法1: 直接获取trending页面
            url = f"https://www.youtube.com/feed/trending?gl=US&hl=en"
            html = self._get_html(url, referer='https://www.youtube.com')

            if not html:
                # 方法2: 尝试通过JSON端点
                # YouTube有内部API可以调用，但这里我们用HTML解析
                print(f"YouTube {self.category} 页面获取失败")
                return topics

            # 尝试多种提取模式
            import json
            import re

            # 模式1: var ytInitialData = ...
            match = re.search(r'var ytInitialData = ({.+?});', html)
            if match:
                try:
                    data = json.loads(match.group(1))
                    topics = self._parse_yt_data(data, count)
                    if topics:
                        print(f"成功获取YouTube {self.category}热门 {len(topics)} 条 (方法1)")
                        return topics
                except:
                    pass

            # 模式2: window["ytInitialData"] = ...
            match = re.search(r'window\[["\']ytInitialData["\']\] = ({.+?});', html)
            if match:
                try:
                    data = json.loads(match.group(1))
                    topics = self._parse_yt_data(data, count)
                    if topics:
                        print(f"成功获取YouTube {self.category}热门 {len(topics)} 条 (方法2)")
                        return topics
                except:
                    pass

            # 模式3: 从script标签中提取
            script_pattern = r'<script[^>]*>(.+?)</script>'
            scripts = re.findall(script_pattern, html, re.DOTALL)

            for script in scripts:
                if 'ytInitialData' in script:
                    try:
                        # 提取JSON部分
                        json_match = re.search(r'ytInitialData\s*=\s*({.+?})\s*;', script)
                        if json_match:
                            data = json.loads(json_match.group(1))
                            topics = self._parse_yt_data(data, count)
                            if topics:
                                print(f"成功获取YouTube {self.category}热门 {len(topics)} 条 (方法3)")
                                return topics
                    except:
                        continue

            # 如果都失败了，尝试用BeautifulSoup解析
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')

                # 查找视频标题
                video_elements = soup.find_all('a', {'id': 'video-title'})
                if video_elements:
                    idx = 1
                    for elem in video_elements[:count]:
                        title = elem.get('title', '').strip()
                        video_id = elem.get('href', '')
                        if video_id.startswith('/watch?v='):
                            video_id = video_id.split('?v=')[1].split('&')[0]

                        if title and self._is_tech_or_education(title):
                            topics.append({
                                'rank': idx,
                                'title': title,
                                'url': f"https://www.youtube.com/watch?v={video_id}",
                                'hot_value': 0,
                                'platform': f'YouTube({self.category})',
                                'category': self.category
                            })
                            idx += 1

                    if topics:
                        print(f"成功获取YouTube {self.category}热门 {len(topics)} 条 (BeautifulSoup)")
                        return topics
            except ImportError:
                pass

            print("未找到YouTube数据")

        except Exception as e:
            print(f"获取YouTube热门时出错: {e}")

        return topics

    def _parse_yt_data(self, data: dict, count: int) -> List[Dict]:
        """解析YouTube数据结构"""
        topics = []
        import re

        try:
            # 导航到视频列表
            contents = (data.get('contents', {})
                       .get('twoColumnBrowseResultsRenderer', {})
                       .get('tabs', [{}])[0]
                       .get('tabRenderer', {})
                       .get('content', {})
                       .get('sectionListRenderer', {})
                       .get('contents', []))

            idx = 1
            for section in contents:
                items = (section.get('itemSectionRenderer', {})
                        .get('contents', []))

                for item in items:
                    if idx > count:
                        break

                    # 尝试多种视频对象类型
                    video = None
                    for key in ['videoRenderer', 'gridVideoRenderer', 'compactVideoRenderer']:
                        if key in item:
                            video = item[key]
                            break

                    if not video:
                        continue

                    # 提取标题
                    title = ''
                    title_obj = video.get('title', {})
                    if 'runs' in title_obj:
                        title = title_obj.get('runs', [{}])[0].get('text', '')
                    elif 'simpleText' in title_obj:
                        title = title_obj.get('simpleText', '')

                    video_id = video.get('videoId', '')
                    if not video_id or not title:
                        continue

                    # 过滤科技/教育相关内容
                    if self._is_tech_or_education(title):
                        # 获取观看数
                        view_count = 0
                        view_text = (video.get('viewCountText', {})
                                    .get('simpleText', '0') or
                                    str(video.get('viewCountText', {})))

                        nums = re.findall(r'[\d,]+', str(view_text))
                        if nums:
                            view_count = int(nums[0].replace(',', ''))

                        topics.append({
                            'rank': idx,
                            'title': title,
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'hot_value': view_count,
                            'platform': f'YouTube({self.category})',
                            'category': self.category
                        })
                        idx += 1

        except (KeyError, IndexError, TypeError) as e:
            print(f"解析YouTube数据结构失败: {e}")

        return topics

    def _is_tech_or_education(self, title: str) -> bool:
        """判断标题是否为科技或教育相关"""
        title_lower = title.lower()

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
            'physics', 'chemistry', 'biology', 'math', 'study'
        ]

        return any(keyword in title_lower for keyword in tech_keywords)
