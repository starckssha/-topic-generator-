# Topic Generator - 网络热点话题聚合工具

自动从多个平台获取网络热点话题并生成Markdown报告。

## 功能特性

- 支持多平台热点话题获取
  - 微博热搜
  - 知乎热榜
  - 今日头条热点
- 自动聚合各平台热点
- 生成结构化的Markdown报告

## 项目结构

```
topicgenerater/
├── src/              # 源代码
│   ├── fetchers/     # 各平台数据获取模块
│   ├── aggregator.py # 数据聚合模块
│   └── exporter.py   # Markdown导出模块
├── tests/            # 测试代码
├── output/           # 输出目录
├── data/             # 数据缓存目录
└── main.py           # 主程序入口
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

生成的Markdown报告将保存在 `output/` 目录中。

## 配置

可以修改 `config.py` 来自定义：
- 获取的话题数量
- 更新频率
- 输出格式
