"""
X(Twitter)趋势抓取器 - 科技/教育话题
"""
from typing import List, Dict
import re
from ..base_fetcher import BaseFetcher


class TwitterFetcher(BaseFetcher):
    """X(Twitter)趋势话题抓取器（科技/教育）"""

    def __init__(self, category: str = 'tech'):
        """
        初始化Twitter抓取器

        Args:
            category: 类别 'tech'(科技) 或 'education'(教育)
        """
        super().__init__()
        self.category = category

    def fetch(self, count: int = 20) -> List[Dict]:
        """
        获取X(Twitter)趋势话题

        Args:
            count: 获取的话题数量

        Returns:
            话题列表
        """
        topics = []

        try:
            print(f"尝试获取X(Twitter) {self.category} 趋势...")

            # 方法1: 尝试从trends页面获取
            url = "https://x.com/i/trends"
            html = self._get_html(url, referer='https://x.com')

            if html:
                topics = self._parse_trends_from_html(html, count)
                if topics:
                    print(f"成功获取X(Twitter) {self.category}趋势 {len(topics)} 条")
                    return topics

            # 方法2: 尝试从首页获取趋势
            url2 = "https://x.com"
            html2 = self._get_html(url2, referer='https://x.com')

            if html2:
                topics = self._parse_trends_from_html(html2, count)
                if topics:
                    print(f"成功获取X(Twitter) {self.category}趋势 {len(topics)} 条 (从首页)")
                    return topics

            # 方法3: 尝试从探索页面
            url3 = "https://x.com/explore"
            html3 = self._get_html(url3, referer='https://x.com')

            if html3:
                topics = self._parse_trends_from_html(html3, count)
                if topics:
                    print(f"成功获取X(Twitter) {self.category}趋势 {len(topics)} 条 (从探索页)")
                    return topics

            print("未能在X(Twitter)页面中找到趋势数据")

        except Exception as e:
            print(f"获取X(Twitter)趋势时出错: {e}")

        return topics

    def _parse_trends_from_html(self, html: str, count: int) -> List[Dict]:
        """从HTML解析趋势数据"""
        topics = []

        try:
            import json

            # 方法1: 尝试提取包含趋势数据的JSON
            # X/Twitter在script标签中存储数据
            script_patterns = [
                r'<script[^>]*>.*?(\{[^<]*"trends"[^<]*\}).*?</script>',
                r'<script[^>]*>.*?window\.__STATE__\s*=\s*({.+?});.*?</script>',
                r'<script[^>]*>.*?self\.__STATE__\s*=\s*({.+?});.*?</script>',
            ]

            for pattern in script_patterns:
                matches = re.findall(pattern, html, re.DOTALL | re.MULTILINE)
                for match in matches:
                    try:
                        # 清理JSON字符串
                        json_str = match.strip()
                        # 移除可能的问题字符
                        json_str = re.sub(r'\\x[0-9a-fA-F]{2}', '', json_str)

                        data = json.loads(json_str)

                        # 尝试提取趋势列表
                        extracted = self._extract_trends_from_json(data, count)
                        if extracted:
                            return extracted
                    except:
                        continue

            # 方法2: 使用正则表达式提取趋势名称
            # X/Twitter的趋势通常在特定的HTML结构中
            trend_patterns = [
                # 趋势名称在href中
                r'<a[^>]*href="/hashtag/([^"]+)"[^>]*><span[^>]*>([^<]+)</span>',
                r'<a[^>]*href="/search\?q=([^"]+)"[^>]*>.*?trend.*?</a>',
                # 直接的文本模式
                r'"name":"([^"]{3,50})"',
                r'"trend_name":"([^"]+)"',
                r'#"<span[^>]*>([^<]+)</span>',
            ]

            all_trends = []
            for pattern in trend_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        # 如果是元组，取第二个元素（通常是显示文本）
                        trend = match[1] if len(match) > 1 else match[0]
                    else:
                        trend = match

                    trend_clean = trend.strip().strip('"')
                    if trend_clean and len(trend_clean) > 2 and len(trend_clean) < 100:
                        all_trends.append(trend_clean)

            # 方法3: 提取hashtag
            hashtag_pattern = r'#([a-zA-Z0-9_\u4e00-\u9fa5]+)'
            hashtags = re.findall(hashtag_pattern, html)
            all_trends.extend([f"#{tag}" for tag in hashtags if len(tag) > 2])

            # 去重并过滤（只过滤明显的垃圾数据）
            seen = set()
            unique_trends = []
            invalid_keywords = [
                'script', 'error', 'failure', 'load', 'undefined',
                'null', 'function', 'object', 'return', 'var',
                '错误', '失败', '加载', '脚本', '错误代码',
                'div', 'span', 'class', 'style', 'width', 'height'
            ]

            for trend in all_trends:
                trend_clean = trend.strip()

                # 过滤掉明显不是趋势的内容
                if (trend_clean and
                    trend_clean not in seen and
                    len(trend_clean) > 2 and
                    len(trend_clean) < 100 and
                    not trend_clean.startswith('http') and
                    not trend_clean.startswith('//') and
                    trend_clean.count(' ') < 10 and  # 避免长句子
                    not any(invalid in trend_clean.lower() for invalid in invalid_keywords)):

                    seen.add(trend_clean)
                    unique_trends.append(trend_clean)

            # 不再过滤科技/教育相关，直接返回所有趋势
            idx = 1
            for trend in unique_trends[:count]:  # 限制数量
                # 创建搜索链接
                search_query = trend.replace('#', '').replace(' ', '%20')
                topics.append({
                    'rank': idx,
                    'title': trend,
                    'url': f"https://x.com/search?q={search_query}&src=trend",
                    'hot_value': 0,  # X不提供公开的热度值
                    'platform': f'X(Twitter, {self.category})',
                    'category': self.category
                })
                idx += 1

        except Exception as e:
            print(f"解析X(Twitter)数据失败: {e}")

        return topics

    def _extract_trends_from_json(self, data: dict, count: int) -> List[Dict]:
        """从JSON数据中提取趋势"""
        topics = []

        def extract_from_dict(obj, depth=0):
            """递归搜索趋势数据"""
            if depth > 10:  # 避免过深递归
                return

            if isinstance(obj, dict):
                # 查找包含趋势的键
                if 'trends' in obj and isinstance(obj['trends'], list):
                    trends = obj['trends']
                    for trend in trends[:count]:
                        if isinstance(trend, dict):
                            name = trend.get('name', '')
                            if name:
                                # 不再过滤科技/教育相关，直接添加
                                topics.append({
                                    'rank': len(topics) + 1,
                                    'title': name,
                                    'url': f"https://x.com/search?q={name}&src=trend",
                                    'hot_value': 0,
                                    'platform': f'X(Twitter, {self.category})',
                                    'category': self.category
                                })

                # 递归搜索
                for value in obj.values():
                    extract_from_dict(value, depth + 1)

            elif isinstance(obj, list):
                for item in obj:
                    extract_from_dict(item, depth + 1)

        extract_from_dict(data)
        return topics[:count]

    def _is_tech_or_education(self, title: str) -> bool:
        """判断标题是否为科技或教育相关"""
        title_lower = title.lower()

        # 科技关键词（包含常见科技标签）
        tech_keywords = [
            '#tech', '#technology', '#ai', '#machinelearning', '#coding',
            '#programming', '#software', '#hardware', '#gadgets', '#startup',
            '#cybersecurity', '#data', '#cloud', '#devops', '#reactjs',
            '#python', '#javascript', '#linux', '#android', '#ios',
            '#blockchain', '#crypto', '#web3', '#metaverse', '#ar',
            '#openai', '#chatgpt', '#gpt', '#llm', '#deeplearning',
            '#technews', '#innovation', '#robotics', '#automation',
            '人工智能', '机器学习', '科技', '编程', '开发者', '技术',
            'chatgpt', 'gpt', 'openai', 'ai', 'artificial intelligence'
        ]

        # 教育关键词
        education_keywords = [
            '#education', '#learning', '#tutorial', '#course', '#study',
            '#science', '#physics', '#chemistry', '#biology', '#math',
            '#history', '#research', '#university', '#students',
            '#onlinelearning', '#edtech', '#stem', '#coding',
            '#knowledge', '#academic', '#school', '#college',
            '教育', '学习', '教程', '课程', '科学', '研究', '大学'
        ]

        # 合并关键词
        keywords = tech_keywords + education_keywords

        # 检查是否包含科技/教育关键词或hashtag
        if any(keyword.lower() in title_lower for keyword in keywords):
            return True

        # 检查是否是纯科技话题（即使没有标签）
        tech_terms = [
            'ai', 'gpt', 'llm', 'api', 'cloud', 'data', 'tech',
            'app', 'software', 'hardware', 'code', 'debug',
            'python', 'javascript', 'react', 'node', 'database',
            'algorithm', 'security', 'network', 'server'
        ]
        if any(term in title_lower for term in tech_terms):
            return True

        return False
