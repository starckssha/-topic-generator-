"""抓取器模块"""
from .weibo_fetcher import WeiboFetcher
from .zhihu_fetcher import ZhihuFetcher
from .toutiao_fetcher import ToutiaoFetcher
from .baidu_fetcher import BaiduFetcher
from .bilibili_fetcher import BilibiliFetcher
from .youtube_fetcher import YouTubeFetcher
from .youtube_api_fetcher import YouTubeAPIFetcher
from .twitter_fetcher import TwitterFetcher
from .hackernews_fetcher import HackerNewsFetcher
from .reddit_fetcher import RedditFetcher

__all__ = [
    'WeiboFetcher',
    'ZhihuFetcher',
    'ToutiaoFetcher',
    'BaiduFetcher',
    'BilibiliFetcher',
    'YouTubeFetcher',
    'YouTubeAPIFetcher',
    'TwitterFetcher',
    'HackerNewsFetcher',
    'RedditFetcher'
]
