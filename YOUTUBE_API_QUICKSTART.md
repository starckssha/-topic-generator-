# YouTube API 集成完成！

## ✅ 已完成的工作

1. ✅ 创建了YouTube Data API v3集成
2. ✅ 创建了API密钥申请指南
3. ✅ 创建了测试脚本
4. ✅ 更新了主程序支持API模式

---

## 🚀 快速开始（3步）

### 步骤1：获取API密钥

请访问 [Google Cloud Console](https://console.cloud.google.com/) 并按照 `docs/YOUTUBE_API_SETUP.md` 中的步骤操作：

1. 创建Google Cloud项目
2. 启用YouTube Data API v3
3. 创建API密钥

**时间：** 约5分钟

### 步骤2：设置API密钥

**Windows PowerShell:**
```powershell
$env:YOUTUBE_API_KEY="你的API密钥"
```

**Windows CMD:**
```cmd
set YOUTUBE_API_KEY=你的API密钥
```

**Linux/Mac:**
```bash
export YOUTUBE_API_KEY="你的API密钥"
```

### 步骤3：测试并运行

```bash
# 测试API连接
python test_youtube_api.py

# 运行主程序（使用YouTube API）
docker run --rm -e USE_PROXY=true -e PROXY_HOST=host.docker.internal -e PROXY_PORT=10810 -e YOUTUBE_API_KEY="你的API密钥" -v "D:\Projects\ClaudeCode\topicgenerater:/app" -w /app python:3.8-slim python main.py
```

---

## 📋 配置选项

### 使用API模式（推荐）

编辑 `config.py`，启用 `youtube_tech_api` 和 `youtube_edu_api`：

```python
'enabled_platforms': [
    'hackernews',
    'youtube_tech_api',   # 使用API获取YouTube科技视频
    'youtube_edu_api',    # 使用API获取YouTube教育视频
    'twitter_tech',
    'twitter_edu',
    'toutiao',
    'bilibili',
    'baidu',
],
```

### 使用HTML模式（备用）

如果没有API密钥，系统会自动回退到HTML解析模式：

```python
'enabled_platforms': [
    'youtube_tech',   # HTML解析模式（不稳定）
    'youtube_edu',
    ...
],
```

---

## 📊 API配额说明

**免费配额：**
- 每天：10,000 API单位
- 获取热门视频列表：100 单位/次
- 获取视频详情：1 单位/个

**实际使用：**
- 运行一次完整抓取：约200-300单位
- **每天可运行约30-50次**

**监控配额：**
- 访问 [Google Cloud Console](https://console.cloud.google.com/)
- API和服务 → 仪表板 → YouTube Data API v3

---

## ❓ 常见问题

### Q1: 如何知道API密钥是否有效？

运行测试脚本：
```bash
python test_youtube_api.py
```

### Q2: 配额用完了怎么办？

免费配额每天自动重置。如需更多，可以在Google Cloud Console中申请增加。

### Q3: 可以同时使用多个API密钥吗？

可以。创建多个API密钥并在代码中轮换使用。

### Q4: API模式和HTML模式有什么区别？

| 特性 | API模式 | HTML模式 |
|------|---------|----------|
| 稳定性 | ✅ 非常稳定 | ❌ 经常变化 |
| 速度 | ✅ 快速 | ⚠️ 较慢 |
| 数据质量 | ✅ 完整准确 | ⚠️ 可能缺失 |
| 配额限制 | ⚠️ 每天10,000次 | ✅ 无限制 |
| 难度 | ⚠️ 需要API密钥 | ✅ 无需配置 |

---

## 📁 文件说明

```
topicgenerater/
├── docs/
│   └── YOUTUBE_API_SETUP.md       # API密钥申请详细指南
├── src/fetchers/
│   ├── youtube_fetcher.py         # HTML解析模式（旧版）
│   └── youtube_api_fetcher.py     # API模式（新版）✨
├── test_youtube_api.py            # API测试脚本
├── config.py                      # 主配置文件
└── config_with_youtube_api.py     # 使用API的配置示例
```

---

## 🎯 下一步

1. **获取API密钥**
   - 参考 `docs/YOUTUBE_API_SETUP.md`

2. **测试连接**
   ```bash
   python test_youtube_api.py
   ```

3. **运行程序**
   ```bash
   # 本地运行
   python main.py

   # Docker运行
   docker run --rm -e USE_PROXY=true -e PROXY_HOST=host.docker.internal -e PROXY_PORT=10810 -e YOUTUBE_API_KEY="你的密钥" -v "D:\Projects\ClaudeCode\topicgenerater:/app" -w /app python:3.8-slim python main.py
   ```

---

## 💡 提示

- **建议：** 优先使用API模式，更稳定可靠
- **备用：** 保留HTML模式作为后备方案
- **安全：** 不要将API密钥提交到Git仓库
- **监控：** 定期检查API使用情况

---

## 📞 帮助

如有问题，请查看：
- `docs/YOUTUBE_API_SETUP.md` - 详细设置指南
- `test_youtube_api.py` - 测试脚本会显示详细错误信息
- [YouTube Data API官方文档](https://developers.google.com/youtube/v3)

---

**祝使用愉快！** 🎉
