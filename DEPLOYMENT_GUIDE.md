# 🌍 服务器部署指南

## 访问方式对比

| 方式 | URL | 谁能访问 |
|------|-----|---------|
| 本地访问 | `http://localhost:5000/` | 只有你的电脑 |
| 局域网访问 | `http://192.168.31.8:5000/` | 同一WiFi的设备 |
| 公网访问 | `http://101.43.15.66/` | 全世界 🌍 |

---

## 🚀 方式三：部署到公网服务器

### 服务器信息
- **IP地址**: 101.43.15.66
- **端口**: 80
- **SSH用户**: root
- **SSH密码**: sx@123456

---

## 📋 部署步骤

### 步骤1：打包项目

在Windows上执行：

```bash
# 进入项目目录
cd D:\Projects\ClaudeCode\topicgenerater

# 使用WinSCP或scp上传到服务器
scp -r . root@101.43.15.66:/var/www/topic-generator
```

**或者使用WinSCP图形界面**：
1. 下载WinSCP: https://winscp.net/
2. 连接到 101.43.15.66 (用户:root, 密码:sx@123456)
3. 上传整个文件夹到 `/var/www/topic-generator/`

---

### 步骤2：SSH登录服务器

**方式A：使用PowerShell**
```powershell
ssh root@101.43.15.66
# 输入密码: sx@123456
```

**方式B：使用工具（推荐）**
- **MobaXterm**: https://mobaxterm.mobatek.net/
- **Xshell**: https://www.xshell.com/zh/xshell/
- **PuTTY**: https://www.putty.org/

---

### 步骤3：在服务器上执行部署

登录后执行：

```bash
# 1. 进入项目目录
cd /var/www/topic-generator

# 2. 给部署脚本添加执行权限
chmod +x deploy.sh

# 3. 执行部署
./deploy.sh
```

**部署脚本会自动完成**：
- ✅ 安装Python依赖
- ✅ 配置Nginx反向代理
- ✅ 创建系统服务
- ✅ 启动服务
- ✅ 设置开机自启

---

### 步骤4：访问系统

**部署成功后，任何设备都可以通过以下URL访问**：

```
http://101.43.15.66/
```

**测试方法**：
- 📱 手机浏览器：打开 http://101.43.15.66/
- 💻 电脑浏览器：打开 http://101.43.15.66/
- 🌍 全球任何地方：打开 http://101.43.15.66/

---

## 🔧 服务器管理命令

### 服务管理

```bash
# 启动服务
sudo systemctl start topic-generator

# 停止服务
sudo systemctl stop topic-generator

# 重启服务
sudo systemctl restart topic-generator

# 查看服务状态
sudo systemctl status topic-generator

# 查看日志
sudo journalctl -u topic-generator -f

# 设置开机自启
sudo systemctl enable topic-generator
```

### Nginx管理

```bash
# 测试配置
sudo nginx -t

# 重载配置
sudo systemctl reload nginx

# 重启Nginx
sudo systemctl restart nginx

# 查看Nginx状态
sudo systemctl status nginx
```

---

## 📱 手机访问演示

### iOS (iPhone/iPad)

1. 打开Safari浏览器
2. 输入：`http://101.43.15.66/`
3. 看到主页界面 ✅

### Android

1. 打开Chrome浏览器
2. 输入：`http://101.43.15.66/`
3. 看到主页界面 ✅

---

## 🐛 常见问题

### Q1：无法访问 http://101.43.15.66/

**原因**：防火墙阻止了80端口

**解决**：
```bash
# 在服务器上开放80端口
sudo ufw allow 80
sudo ufw allow 5000
sudo ufw status
```

**腾讯云控制台**：
1. 登录腾讯云：https://console.cloud.tencent.com/
2. 进入：云服务器 → 安全组
3. 添加规则：
   - 协议：TCP
   - 端口：80
   - 来源：0.0.0.0/0

### Q2：服务启动失败

**查看日志**：
```bash
sudo journalctl -u topic-generator -n 50
```

**常见错误**：
- 端口5000被占用：`sudo lsof -i:5000` 查看占用进程
- Python模块缺失：`pip3 install -r requirements.txt`
- 数据库连接失败：检查数据库配置

### Q3：页面无法加载API

**检查Nginx配置**：
```bash
sudo nginx -t
sudo systemctl reload nginx
```

**检查Flask服务**：
```bash
sudo systemctl status topic-generator
```

---

## 🔐 安全建议

### 1. 修改SSH密码

```bash
# 登录服务器后
passwd
# 输入新密码
```

### 2. 配置防火墙

```bash
# 只开放必要的端口
sudo ufw enable
sudo ufw allow ssh    # SSH端口22
sudo ufw allow http   # HTTP端口80
sudo ufw allow 5000   # Flask端口
```

### 3. 使用HTTPS（可选）

```bash
# 安装Let's Encrypt证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d 101.43.15.66
```

---

## 📊 性能优化

### 1. 使用Gunicorn（生产环境推荐）

```bash
# 安装Gunicorn
pip3 install gunicorn

# 启动服务（替代Flask开发服务器）
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

### 2. 配置Nginx缓存

在Nginx配置中添加：
```nginx
location /static {
    alias /var/www/topic-generator/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 🎉 部署成功后

你的系统将会：
- ✅ 24小时在线运行
- ✅ 全球可访问
- ✅ 开机自动启动
- ✅ 自动重启崩溃的服务

访问地址：**http://101.43.15.66/**

---

## 📞 技术支持

如果遇到问题，检查：
1. 服务状态：`sudo systemctl status topic-generator`
2. Nginx状态：`sudo systemctl status nginx`
3. 日志：`sudo journalctl -u topic-generator -f`
4. 防火墙：`sudo ufw status`

---

生成时间：2026-01-18
服务器：101.43.15.66:80
