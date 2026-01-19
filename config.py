"""
配置文件
"""
CONFIG = {
    # API密钥配置
    'youtube_api_key': 'AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk',
    'deepseek_api_key': 'sk-aXWs0YDBq79J7Xx59aD6993bCa4e4a86813eE2Fa1eFd110d',

    # 数据库配置
    'db_host': 'sh-cdb-qkm4h7s0.sql.tencentcdb.com',
    'db_port': 27339,
    'db_user': 'root',
    'db_password': 'sx@123456',  # 你的腾讯云数据库密码
    'db_name': 'topic_generator',

    # 代理配置（用于访问YouTube/Twitter等需要VPN的服务）
    # 如果你的VPN端口不是7890，请修改为你的端口
    # 常见端口：7890(Clash), 10808, 10809, 7891等
    'use_proxy': True,
    'http_proxy': 'http://127.0.0.1:7890',
    'https_proxy': 'http://127.0.0.1:7890',

    # 各平台获取的话题数量（增加数量以获得更多话题）
    'weibo_count': 50,
    'zhihu_count': 50,
    'toutiao_count': 50,
    'baidu_count': 50,
    'bilibili_count': 50,
    'youtube_count': 50,
    'twitter_count': 50,
    'hackernews_count': 50,
    'reddit_count': 50,  # 新增

    # 启用的平台（启用所有可用平台）
    'enabled_platforms': [
        'hackernews',  # Hacker News - 科技新闻（无需认证，推荐）
        'reddit_tech',  # Reddit科技新闻（无需认证，推荐）
        'reddit_programming',  # Reddit编程（无需认证，推荐）
        'reddit_ai',  # Reddit AI（无需认证，推荐）
        'toutiao',    # 今日头条
        'bilibili',   # B站
        'baidu',      # 百度
        'twitter_tech', # X(Twitter)科技趋势（HTML解析）
        'twitter_edu',  # X(Twitter)教育趋势（HTML解析）
        'youtube_tech_api',  # YouTube科技频道（需要API密钥）
        'youtube_edu_api',   # YouTube教育频道（需要API密钥）
        # 'youtube_tech', # YouTube科技频道（HTML解析，不稳定）
        # 'youtube_edu',  # YouTube教育频道（HTML解析，不稳定）
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
}
