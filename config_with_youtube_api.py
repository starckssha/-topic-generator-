"""
配置文件 - 使用YouTube API版本
"""
CONFIG = {
    # 各平台获取的话题数量
    'weibo_count': 20,
    'zhihu_count': 20,
    'toutiao_count': 20,
    'baidu_count': 20,
    'bilibili_count': 20,
    'youtube_count': 20,
    'twitter_count': 20,
    'hackernews_count': 20,

    # 启用的平台
    # 使用YouTube API获取数据（更稳定、更准确）
    'enabled_platforms': [
        'hackernews',  # Hacker News - 科技新闻（无需认证，推荐）
        'youtube_tech_api',  # YouTube科技频道（使用API）
        'youtube_edu_api',   # YouTube教育频道（使用API）
        'twitter_tech', # X(Twitter)科技趋势
        'twitter_edu',  # X(Twitter)教育趋势
        # 通用平台也可用
        'toutiao',
        'bilibili',
        'baidu',
        # 'weibo',   # 需要认证
        # 'zhihu',   # 需要认证
    ],

    # 话题分类过滤
    'categories': {
        'tech': True,       # 科技类
        'education': True,  # 教育类
        'general': True,    # 通用类
    },

    # 输出目录
    'output_dir': 'output',
    'data_dir': 'data',

    # 请求超时时间（秒）
    'timeout': 15,

    # YouTube API配置
    'youtube_api_key': None,  # 从环境变量YOUTUBE_API_KEY获取，或在此设置
}
