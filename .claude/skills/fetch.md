# 热点抓取 Skill

触发热点话题抓取任务，从多个平台获取最新热点。

## 使用方法

```bash
/fetch
```

## 功能说明

- 从多个平台抓取热点话题
- 平台包括：HackerNews, Reddit, 今日头条, B站, 百度, Twitter, YouTube
- 自动保存到数据库
- 显示抓取进度和结果

## 配置

需要在 `config.py` 中配置：
- 启用的平台 (`enabled_platforms`)
- 各平台话题数量
- API密钥 (如YouTube, DeepSeek)

## 示例

```bash
# 抓取所有启用的平台
/fetch

# 仅抓取HackerNews
# (在config.py中设置enabled_platforms = ['hackernews'])
```
