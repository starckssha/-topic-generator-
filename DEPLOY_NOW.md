# 🚀 立即部署到Railway

## ✅ 已完成的准备工作

1. ✅ Git仓库已初始化
2. ✅ 代码已提交
3. ✅ Dockerfile已创建
4. ✅ railway.toml配置已创建
5. ✅ 数据库连接支持MySQL和PostgreSQL
6. ✅ requirements.txt已更新

## 📋 下一步操作

### 第一步：推送到GitHub

```bash
# 1. 在GitHub创建新仓库
# 访问 https://github.com/new
# 仓库名：topic-generator (或其他名称)
# 不要初始化README

# 2. 添加远程仓库（替换YOUR_USERNAME）
cd D:\Projects\ClaudeCode\topicgenerater
git remote add origin https://github.com/YOUR_USERNAME/topic-generator.git

# 3. 推送代码
git branch -M main
git push -u origin main
```

### 第二步：在Railway部署

1. **访问Railway**
   - 打开 https://railway.app/
   - 点击 "Start a New Project"
   - 使用GitHub账号登录

2. **部署项目**
   - 选择 "Deploy from GitHub repo"
   - 选择 `topic-generator` 仓库
   - Railway会自动检测Dockerfile

3. **添加PostgreSQL数据库**
   - 在项目页面点击 "New Service"
   - 选择 "Database" → "Add PostgreSQL"
   - 等待数据库创建完成

4. **配置环境变量**
   - 点击你的web服务（不是数据库）
   - 进入 "Variables" 标签
   - 点击 "New Variable"
   - 添加以下变量：

```bash
# 从PostgreSQL服务获取（点击数据库 → Variables → 复制值）
DB_HOST = [复制PGHOST的值]
DB_PORT = 5432
DB_USER = postgres
DB_PASSWORD = [复制PGPASSWORD的值]
DB_NAME = railway

# API密钥（已有）
DEEPSEEK_API_KEY = sk-aXWs0YDBq79J7Xx59aD6993bCa4e4a86813eE2Fa1eFd110d
YOUTUBE_API_KEY = AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk
```

### 第三步：运行数据库迁移

1. 在Railway项目页面
2. 点击你的web服务
3. 点击 "Console" 标签
4. 点击 "Open New Console"
5. 运行迁移命令：

```bash
python scripts/add_first_generated_at.py
```

### 第四步：访问应用

部署完成后，Railway会提供一个URL：

```
https://your-app-name.up.railway.app
```

点击访问即可！

## 📊 验证部署

访问以下URL测试功能：

- 主页：`https://your-app.up.railway.app/`
- 抓取API：`https://your-app.up.railway.app/api/fetch/results`
- 生成API：`https://your-app.up.railway.app/api/generate/available-topics?limit=5`

## 🔄 自动更新

以后每次推送代码到GitHub，Railway会自动重新部署：

```bash
git add .
git commit -m "更新功能"
git push
# Railway自动部署！
```

## 🆘 常见问题

### Q1: 推送GitHub失败？
```bash
# 确认GitHub token已设置
git remote -v
# 如果需要，重新添加remote
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/topic-generator.git
```

### Q2: Railway部署失败？
1. 点击项目 → View Logs查看错误
2. 检查requirements.txt是否完整
3. 检查Dockerfile语法是否正确

### Q3: 数据库连接失败？
1. 确认环境变量已正确设置
2. 确认PostgreSQL服务正在运行
3. 尝试重新部署

### Q4: 如何查看数据库内容？
1. 点击PostgreSQL服务
2. 点击 "Query" 标签
3. 执行SQL查询：

```sql
SELECT COUNT(*) FROM hot_topics;
SELECT * FROM hot_topics ORDER BY fetched_at DESC LIMIT 10;
```

## 💰 费用说明

- **免费额度**：$5/月
  - 512MB RAM
  - 1GB 存储
  - 每月约500小时运行时间
- **超出后**：按量计费，通常$5-10/月

对于个人使用，免费额度完全够用！

## 📞 需要帮助？

- Railway文档：https://docs.railway.app/
- 查看详细部署文档：`Railway.deploy.md`
- 查看快速开始：`QUICK_START.md`

---

**准备好了吗？开始部署吧！** 🚀
