# Railway 部署指南

## 1. 准备工作

### 安装Railway CLI (可选)
```bash
npm install -g @railway/cli
```

### 创建 railway.toml 配置文件
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "python web_server.py"
healthcheckPath = "/"

[env]
PORT = "5000"
```

## 2. Dockerfile (Railway需要)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "web_server.py"]
```

## 3. requirements.txt (需要完整)

```txt
Flask==3.0.0
Flask-CORS==4.0.0
pymysql==1.1.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==5.1.0
```

## 4. 环境变量设置

在Railway控制面板设置以下环境变量：

```bash
# 数据库配置
DB_HOST=your-railway-postgres-host.railway.app
DB_PORT=5432  # Railway使用PostgreSQL，不是MySQL
DB_USER=postgres
DB_PASSWORD=your-password
DB_NAME=railway

# API密钥
DEEPSEEK_API_KEY=sk-aXWs0YDBq79J7Xx59aD6993bCa4e4a86813eE2Fa1eFd110d
YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk

# 代理配置（如果需要）
USE_PROXY=false
```

## 5. 部署步骤

### 方式1: 通过GitHub (推荐)
1. 将代码推送到GitHub
2. 访问 railway.app
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择你的仓库
6. Railway自动检测并部署

### 方式2: 通过CLI
```bash
# 登录
railway login

# 初始化项目
railway init

# 添加PostgreSQL数据库
railway add postgresql

# 设置环境变量
railway variables set DB_HOST=$(railway variables get PGHOST)
railway variables set DB_PORT=5432
railway variables set DB_USER=postgres
railway variables set DB_PASSWORD=$(railway variables get PGPASSWORD)
railway variables set DB_NAME=railway

# 部署
railway up
```

## 6. 数据库迁移

部署后需要运行迁移：

```bash
# 在Railway控制台打开Console
railway open console

# 运行迁移脚本
python scripts/add_first_generated_at.py
```

## 7. 访问应用

部署成功后，Railway会提供一个URL：
```
https://your-app.railway.app
```

## 8. 定时任务设置

Railway目前不支持Cron jobs，需要使用外部服务：

### 选项1: GitHub Actions
```yaml
# .github/workflows/daily-fetch.yml
name: Daily Fetch
on:
  schedule:
    - cron: '0 0 * * *'  # 每天0点
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger API
        run: |
          curl -X POST https://your-app.railway.app/api/fetch/start
```

### 选项2: EasyCron (免费)
```bash
1. 访问 easycron.com
2. 添加定时任务
3. URL: https://your-app.railway.app/api/fetch/start
4. 设置每天8点执行
```

## 费用说明

- 免费额度：$5/月
  - 512MB RAM
  - 1GB 存储
  - 有限的小时数

- 超出后按量付费，通常$5-10/月足够

## 注意事项

1. **数据库从MySQL改为PostgreSQL**
   - Railway内置PostgreSQL
   - 需要修改连接代码（使用psycopg2代替pymysql）
   - SQL语法基本兼容

2. **文件存储限制**
   - Railway文件系统是临时的
   - 建议使用Railway的Volume或对象存储

3. **日志查看**
   ```bash
   railway logs  # 查看实时日志
   ```

4. **重启服务**
   ```bash
   railway restart
   ```
