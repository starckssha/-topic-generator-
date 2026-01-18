# 使用说明

## 项目简介

Topic Generator 是一个网络热点话题聚合工具，能够自动从多个主流平台获取实时热点话题，并生成结构化的Markdown报告。

## 支持的平台

目前支持以下平台（按成功率排序）：

| 平台 | 状态 | 说明 |
|------|------|------|
| 今日头条 | ✓ 稳定 | API访问正常 |
| B站热门 | ✓ 稳定 | API访问正常 |
| 百度热搜 | △ 可用 | 部分数据可用 |
| 微博热搜 | ✗ 受限 | 需要Cookie认证 |
| 知乎热榜 | ✗ 受限 | 需要登录认证 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python main.py
```

### 3. 查看报告

生成的报告会保存在 `output/` 目录中，文件名格式为 `hot_topics_YYYYMMDD_HHMMSS.md`

## 配置说明

编辑 `config.py` 可以自定义以下配置：

```python
CONFIG = {
    # 各平台获取的话题数量
    'weibo_count': 20,
    'zhihu_count': 20,
    'toutiao_count': 20,
    'baidu_count': 20,
    'bilibili_count': 20,

    # 启用的平台（可以注释掉不需要的平台）
    'enabled_platforms': [
        'toutiao',  # 今日头条
        'baidu',    # 百度
        'bilibili', # B站
        # 'weibo',   # 微博（需要认证）
        # 'zhihu',   # 知乎（需要认证）
    ],

    # 输出目录
    'output_dir': 'output',

    # 请求超时时间（秒）
    'timeout': 15,
}
```

## 高级配置

### 启用微博和知乎

微博和知乎需要额外的认证，你可以：

1. **方法一：在代码中添加Cookie**

   编辑 `src/base_fetcher.py`，在 `_setup_session` 方法中添加：
   ```python
   self.session.headers.update({
       'Cookie': '你的Cookie值'
   })
   ```

2. **方法二：使用第三方RSS源**

   可以使用提供RSS热榜的第三方服务

### 自定义输出格式

编辑 `src/exporter.py` 可以自定义Markdown输出格式

## 输出示例

生成的报告包含以下部分：

- **数据概览**：总计话题数、平台数量、跨平台热点数
- **跨平台热点**：在多个平台同时出现的话题
- **各平台热点**：按平台分组的热点列表，包含标题、链接、热度值

## 常见问题

### 1. 为什么某些平台获取失败？

答：部分平台（如微博、知乎）需要登录认证。目前程序已经尝试多个备用API，但如果仍然失败，可能需要添加Cookie认证。

### 2. 如何提高成功率？

答：
- 使用网络代理
- 添加Cookie认证
- 调整请求超时时间
- 减少并发请求数

### 3. 报告在哪里？

答：默认保存在 `output/` 目录，可以在 `config.py` 中修改 `output_dir` 配置。

## 项目结构

```
topicgenerater/
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── requirements.txt       # 依赖列表
├── README.md             # 项目说明
├── USAGE.md              # 本文件
├── output/               # 输出目录
└── src/
    ├── base_fetcher.py   # 基础抓取器
    ├── aggregator.py     # 话题聚合器
    ├── exporter.py       # Markdown导出器
    └── fetchers/         # 各平台抓取器
        ├── weibo_fetcher.py
        ├── zhihu_fetcher.py
        ├── toutiao_fetcher.py
        ├── baidu_fetcher.py
        └── bilibili_fetcher.py
```

## 开发计划

- [ ] 添加更多平台支持
- [ ] 支持定时任务
- [ ] 添加Web界面
- [ ] 支持数据可视化
- [ ] 添加历史数据存储

## 许可证

MIT License
