# 🚀 快速部署到Railway

## 5分钟部署步骤

### 1️⃣ 推送代码到GitHub
```bash
git add .
git commit -m "准备Railway部署"
git push origin main
```

### 2️⃣ 在Railway创建项目
1. 访问 [railway.app](https://railway.app/)
2. 点击 "Start a New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的仓库

### 3️⃣ 添加数据库
1. 在项目页面点击 "New Service"
2. 选择 "Database" → "Add PostgreSQL"
3. Railway会自动创建数据库

### 4️⃣ 配置环境变量
1. 点击你的web服务
2. 进入 "Variables" 标签
3. 添加以下变量：

```bash
# 从PostgreSQL服务自动获取
DB_HOST=点击数据库 → Variables → PGHOST
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=点击数据库 → Variables → PGPASSWORD
DB_NAME=railway

# API密钥
DEEPSEEK_API_KEY=sk-aXWs0YDBq79J7Xx59aD6993bCa4e4a86813eE2Fa1eFd110d
YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk
```

### 5️⃣ 运行数据库迁移
Railway部署后，需要执行数据库迁移：

**方式1: 通过Railway Console**
```bash
1. 在Railway项目页面
2. 点击你的web服务
3. 点击 "Console" 标签
4. 点击 "Open New Console"
5. 运行: python scripts/add_first_generated_at.py
```

**方式2: 通过本地SSH**
```bash
railway open console
python scripts/add_first_generated_at.py
```

### 6️⃣ 访问应用
部署成功后，Railway会提供URL：
```
https://your-project-name.up.railway.app
```

## 📊 监控和日志

### 查看日志
```bash
# 通过CLI
railway logs

# 或在网页界面
点击服务 → View Logs
```

### 查看指标
- CPU使用率
- 内存使用
- 请求次数
- 响应时间

## 🔄 更新部署

每次推送代码到GitHub，Railway会自动重新部署！

```bash
git add .
git commit -m "更新功能"
git push
# Railway自动检测并部署
```

## 💰 费用说明

- 免费额度：$5/月
- 包含：
  - 512MB RAM
  - 1GB 存储
  - 有限运行时间
- 通常个人项目完全够用

## ⚠️ 重要提示

### 1. 数据库从MySQL改为PostgreSQL
Railway使用PostgreSQL，需要修改数据库连接：

**src/database/connection.py**
```python
# 修改前 (MySQL)
DB_CONFIG = {
    'host': ...,
    'port': 3306,
    'user': ...,
    'password': ...,
    'database': ...,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 修改后 (PostgreSQL)
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}
```

**或者同时支持两种数据库：**
```python
DB_TYPE = os.getenv('DB_TYPE', 'mysql')  # 'mysql' or 'postgresql'

if DB_TYPE == 'postgresql':
    import psycopg2
    from psycopg2.extras import RealDictCursor
    # 使用PostgreSQL
else:
    import pymysql
    # 使用MySQL
```

### 2. 定时任务
Railway不支持Cron，使用外部服务：

**推荐: EasyCron**
1. 注册 easycron.com
2. 添加Cron任务
3. URL: `https://your-app.up.railway.app/api/fetch/start`
4. 设置: 每天8:00执行

## 🆘 常见问题

### Q: 部署失败怎么办？
A:
1. 查看日志: `railway logs`
2. 检查requirements.txt是否完整
3. 检查Dockerfile是否正确

### Q: 数据库连接失败？
A:
1. 检查环境变量是否正确
2. 确认PostgreSQL服务正在运行
3. 尝试在Console测试连接

### Q: 如何查看数据库内容？
A:
1. 点击PostgreSQL服务
2. 点击 "Query" 标签
3. 执行SQL查询

### Q: 超出免费额度会怎样？
A:
1. 服务会暂停
2. 升级到付费计划或等待下个月重置
3. 付费计划约$5/月起

## 📞 需要帮助？

- Railway文档: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- 或查看 `Railway.deploy.md` 详细文档
