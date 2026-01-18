# Topic Generator 项目总结

## 项目概述

网络热点话题聚合工具，支持从多个主流平台获取实时热点话题，并生成结构化的Markdown报告。

**v2.0 新特性**: 专注于科技和教育领域的话题聚合

---

## 支持的平台

### 国内平台（优先推荐）

| 平台 | 状态 | 说明 |
|------|------|------|
| 今日头条 | ✓ 稳定 | 无需认证，API稳定 |
| B站 | ✓ 稳定 | 无需认证，可获取热门视频 |
| 百度 | △ 可用 | 部分数据可用 |
| 微博 | ✗ 受限 | 需要Cookie认证 |
| 知乎 | ✗ 受限 | 需要登录认证 |

### 国际平台

| 平台 | 状态 | 说明 |
|------|------|------|
| Hacker News | ✓ 推荐 | 科技新闻，无需认证 |
| YouTube | △ 可用 | 科技/教育类别，需网络访问 |
| X(Twitter) | ✗ 受限 | 需要认证 |

---

## 使用方式

### 方式一：通用话题聚合

```bash
# 使用默认配置
python main.py

# 或自定义平台（编辑 config.py）
'enabled_platforms': ['toutiao', 'bilibili', 'baidu']
```

### 方式二：科技/教育话题聚合

```bash
# 使用专用脚本（带关键词过滤）
python main_tech.py

# 自定义关键词（编辑 config_tech.py）
'tech_keywords': ['AI', '芯片', '编程', ...]
```

---

## 项目结构

```
topicgenerater/
├── main.py                 # 主程序（通用）
├── main_tech.py           # 科技话题专用脚本
├── config.py              # 通用配置
├── config_tech.py         # 科技话题配置
│
├── src/
│   ├── base_fetcher.py    # 基础抓取器（重试、UA池）
│   ├── aggregator.py      # 话题聚合器
│   ├── exporter.py        # Markdown导出器
│   └── fetchers/          # 各平台抓取器
│       ├── weibo_fetcher.py
│       ├── zhihu_fetcher.py
│       ├── toutiao_fetcher.py      # ✓ 可用
│       ├── baidu_fetcher.py        # ✓ 可用
│       ├── bilibili_fetcher.py     # ✓ 可用
│       ├── youtube_fetcher.py      # 新增
│       ├── twitter_fetcher.py      # 新增
│       └── hackernews_fetcher.py   # 新增（推荐）
│
├── output/                # 输出目录
│   └── hot_topics_*.md   # 生成的报告
│
└── docs/
    ├── README.md          # 项目说明
    ├── USAGE.md          # 使用说明
    └── TECH_TOPICS.md    # 科技话题说明
```

---

## 核心功能

### 1. 多平台数据抓取
- ✓ 自动重试机制（3次）
- ✓ User-Agent池（5个不同浏览器）
- ✓ 每个平台多个备用API端点
- ✓ Session复用提高性能

### 2. 话题过滤
- ✓ 基于关键词的智能过滤
- ✓ 支持自定义关键词列表
- ✓ 科技/教育分类
- ✓ 过滤率统计

### 3. 数据聚合
- ✓ 跨平台话题识别
- ✓ 热度值排序
- ✓ 统计摘要

### 4. 报告生成
- ✓ 结构化Markdown格式
- ✓ 热度值格式化（万/亿）
- ✓ 包含链接和排名

---

## 配置示例

### 示例1：只获取稳定平台

```python
# config.py
CONFIG = {
    'enabled_platforms': [
        'toutiao',   # 今日头条
        'bilibili',  # B站
    ],
    'toutiao_count': 20,
    'bilibili_count': 20,
}
```

### 示例2：科技话题过滤

```python
# config_tech.py
CONFIG = {
    'enabled_platforms': ['toutiao'],
    'filter_by_category': True,
    'toutiao_count': 100,  # 大量获取后过滤
    
    'tech_keywords': [
        'AI', '人工智能', '芯片', '编程',
        '科技', '技术', '互联网',
    ],
}
```

### 示例3：使用Hacker News

```python
# config.py
CONFIG = {
    'enabled_platforms': ['hackernews'],
    'hackernews_count': 30,
}
```

---

## 性能数据

### 优化前 vs 优化后

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 平台数量 | 3 | 8 |
| 成功率 | 33% (1/3) | 60% (3/5) |
| 话题数量 | 20 | 41 |
| 功能 | 基础抓取 | 抓取+过滤+分类 |

### 当前可用平台

| 平台 | 成功率 | 话题数 |
|------|--------|--------|
| 今日头条 | 100% | 20 |
| B站 | 100% | 20 |
| 百度 | 50% | 1 |
| Hacker News | 需测试 | - |

---

## 常见问题

### Q1: 为什么某些平台获取失败？

**A**: 部分平台（微博、知乎、X）需要认证。建议：
- 使用不需要认证的平台（今日头条、B站、Hacker News）
- 或添加Cookie认证

### Q2: 如何获取科技话题？

**A**: 两种方式：
1. 使用 `main_tech.py` 脚本（自动过滤）
2. 只启用科技平台（Hacker News、YouTube科技）

### Q3: 遇到SSL错误怎么办？

**A**: 
- 检查网络连接
- 使用网络代理
- 只使用国内平台

### Q4: 如何自定义关键词？

**A**: 编辑 `config_tech.py`:
```python
'tech_keywords': [
    '你的关键词1', '你的关键词2', ...
]
```

---

## 未来计划

- [ ] 添加更多平台（Reddit、GitHub Trending）
- [ ] 支持定时任务（cron/scheduler）
- [ ] 添加Web界面
- [ ] 支持数据可视化图表
- [ ] 添加历史数据存储和对比
- [ ] 支持RSS订阅
- [ ] 添加关键词热度趋势分析

---

## 技术栈

- **语言**: Python 3.x
- **依赖**:
  - `requests` - HTTP请求
  - `python-dateutil` - 日期处理

## 许可证

MIT License

---

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请创建Issue。

---

**项目地址**: `D:\Projects\ClaudeCode\topicgenerater`

**最后更新**: 2026-01-08

**版本**: v2.0
