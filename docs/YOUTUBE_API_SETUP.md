# YouTube Data API v3 设置指南

## 📋 概述

YouTube Data API v3 提供了官方的数据访问接口，可以获取视频信息、频道数据、评论、热门视频等。

**免费配额：**
- 每天：10,000 API 单位
- 每次获取热门视频列表：100 单位
- 每次获取视频详情：1 单位
- **足够每天获取约100次热门视频数据**

---

## 🔑 获取API密钥

### 步骤1：创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 登录你的Google账号
3. 点击顶部的项目选择器，选择"新建项目"
4. 项目名称填写：`Topic Generator`（或其他名称）
5. 点击"创建"

### 步骤2：启用YouTube Data API v3

1. 在Google Cloud Console中，确保选择了刚创建的项目
2. 点击左侧菜单的"API和服务" → "库"
3. 搜索"YouTube Data API v3"
4. 点击进入，然后点击"启用"按钮
5. 等待几分钟直到API启用完成

### 步骤3：创建API密钥

1. 在左侧菜单中，点击"凭据"
2. 点击顶部的"+ 创建凭据"按钮
3. 选择"API密钥"
4. 系统会自动创建一个API密钥，格式类似：`AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
5. **复制这个密钥并保存好**（关闭窗口后将无法再次查看完整密钥）

### 步骤4：限制API密钥（可选但推荐）

1. 在凭据页面，点击刚创建的API密钥
2. 在"应用限制"部分：
   - 选择"IP地址"
   - 添加你的服务器IP或留空（如果不确定）
3. 在"API限制"部分：
   - 选择"限制密钥"
   - 从下拉菜单中选择"YouTube Data API v3"
4. 点击"保存"

---

## ⚙️ 配置Topic Generator

### 方法1：环境变量（推荐）

1. 打开终端/命令行
2. 设置环境变量：
   ```bash
   # Windows (PowerShell)
   $env:YOUTUBE_API_KEY="你的API密钥"

   # Windows (CMD)
   set YOUTUBE_API_KEY=你的API密钥

   # Linux/Mac
   export YOUTUBE_API_KEY="你的API密钥"
   ```
3. 运行程序

### 方法2：配置文件

1. 编辑 `config_youtube_api.py` 文件
2. 将你的API密钥填入：
   ```python
   CONFIG = {
       'youtube_api_key': '你的API密钥',
       ...
   }
   ```

---

## 🧪 测试API密钥

### 快速测试

访问以下URL（替换YOUR_API_KEY）：
```
https://www.googleapis.com/youtube/v3/videos?part=snippet&id=dQw4w9WgXcQ&key=YOUR_API_KEY
```

如果返回JSON数据（包含视频信息），说明密钥有效。

### 使用测试脚本

```bash
python test_youtube_api.py
```

---

## 📊 API配额监控

### 查看使用情况

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 进入你的项目
3. 点击"API和服务" → "仪表板"
4. 选择"YouTube Data API v3"
5. 查看"请求"图表和配额使用情况

### 优化配额使用

- 启用缓存：避免重复请求相同数据
- 批量请求：一次获取多个视频信息
- 合理设置更新频率：建议每小时更新一次

---

## 🛡️ 安全建议

1. **不要将API密钥提交到Git仓库**
   - 已将`config_youtube_api.py`添加到`.gitignore`
   - 使用环境变量或本地配置文件

2. **定期轮换密钥**
   - 每90天重新生成一次密钥

3. **监控使用情况**
   - 如发现异常使用立即禁用密钥

4. **设置配额上限**
   - 在Google Cloud Console中设置每日配额上限
   - 避免意外超支

---

## ❓ 常见问题

### Q1: 配额用完了怎么办？

**A:**
- 免费配额每天自动重置
- 如需更多，可升级为付费计划（但通常不需要）

### Q2: API密钥泄露了怎么办？

**A:**
- 立即在Google Cloud Console中删除该密钥
- 创建新的API密钥
- 更新所有使用该密钥的应用

### Q3: 可以在多个项目中使用同一个密钥吗？

**A:**
- 技术上可以，但不建议
- 建议为每个项目创建独立的密钥
- 便于追踪和管理

### Q4: API请求失败怎么办？

**A:**
- 检查密钥是否正确
- 查看配额是否用尽
- 确认API已启用
- 检查网络连接

---

## 📚 参考文档

- [YouTube Data API v3 官方文档](https://developers.google.com/youtube/v3)
- [API配额详情](https://developers.google.com/youtube/v3/determine_quota_cost)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## ✅ 下一步

1. 按照上述步骤获取API密钥
2. 运行测试脚本验证配置：
   ```bash
   python test_youtube_api.py
   ```
3. 运行主程序获取YouTube热门视频：
   ```bash
   python main.py
   ```

如有问题，请查看 `test_youtube_api.py` 中的错误信息。
