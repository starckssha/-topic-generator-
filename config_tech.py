"""
科技/教育话题配置文件
"""
CONFIG = {
    # 使用已验证可用的平台
    'enabled_platforms': [
        'toutiao',  # 今日头条（之前验证可用）
    ],

    # 启用话题过滤，只保留科技/教育相关话题
    'filter_by_category': True,
    'categories': {
        'tech': True,       # 科技
        'education': True,  # 教育
        'general': False,   # 通用（不启用）
    },

    # 今日话题数量
    'toutiao_count': 100,  # 获取更多用于过滤

    # 科技关键词（用于过滤）
    'tech_keywords': [
        '科技', '技术', 'AI', '人工智能', '芯片', '半导体',
        '软件', '硬件', '互联网', '5G', '6G', '云计算',
        '大数据', '区块链', '元宇宙', '量子', '机器人',
        '编程', '代码', '开发', '算法', '数据',
        '手机', '电脑', '智能', '新能源', '汽车',
        'tech', 'technology', 'ai', 'coding', 'software',
        'algorithm', 'data', 'cloud', 'programming'
    ],

    # 教育关键词
    'education_keywords': [
        '教育', '学习', '教程', '课程', '大学', '研究',
        '科学', '物理', '化学', '生物', '数学', '历史',
        '培训', '考试', '学生', '老师', '学校',
        'education', 'learning', 'tutorial', 'course', 'study',
        'science', 'research', 'university'
    ],

    # 输出目录
    'output_dir': 'output',
    'data_dir': 'data',

    # 请求超时时间（秒）
    'timeout': 15,
}
