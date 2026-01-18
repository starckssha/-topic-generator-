"""
VPN环境配置 - 使用国际平台
"""
CONFIG = {
    # 启用国际平台
    'enabled_platforms': [
        'hackernews',      # Hacker News - 科技新闻（推荐）
        'youtube_tech',    # YouTube 科技
        'youtube_edu',     # YouTube 教育
    ],

    # 各平台获取的话题数量
    'hackernews_count': 30,
    'youtube_count': 20,

    # 输出目录
    'output_dir': 'output',
    'data_dir': 'data',

    # 请求超时时间（秒）
    'timeout': 20,
}
