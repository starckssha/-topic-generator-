# GitHub Pages 部署指南

## 📱 将小红书爆文助手部署到公网

### 方案1：使用GitHub Pages（推荐，完全免费）

#### 步骤1：创建GitHub仓库

1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 仓库名称：`xiaohongshu-posts`（或其他名称）
4. 设置为 **Public**（公开）
5. **不要**勾选 "Add a README file"
6. 点击 "Create repository"

#### 步骤2：准备部署文件

在项目目录运行以下命令：

```bash
# 1. 进入h5目录
cd h5

# 2. 初始化git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit"

# 5. 关联到GitHub仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/xiaohongshu-posts.git

# 6. 推送到GitHub
git branch -M main
git push -u origin main
```

#### 步骤3：启用GitHub Pages

1. 访问你的GitHub仓库页面
2. 点击 **Settings**（设置）
3. 左侧菜单找到 **Pages**
4. **Source** 下选择：
   - Branch: `main`
   - Folder: `/root`
5. 点击 **Save**

#### 步骤4：获取访问地址

等待1-2分钟后，GitHub Pages会生成访问地址：

```
https://YOUR_USERNAME.github.io/xiaohongshu-posts/
```

这个地址可以：
- ✅ 在手机浏览器直接打开
- ✅ 分享到微信/小红书
- ✅ 永久免费使用

---

### 方案2：使用Vercel（更简单）

#### 步骤1：安装Vercel CLI

```bash
npm install -g vercel
```

#### 步骤2：部署

```bash
cd h5
vercel
```

按照提示操作即可，完成后会得到：
```
https://xiaohongshu-posts.vercel.app
```

---

### 方案3：使用Netlify（拖拽部署）

1. 访问 https://www.netlify.com
2. 注册账号
3. 将 `h5` 文件夹**整个拖拽**到Netlify页面
4. 等待部署完成，获得地址：
   ```
   https://random-name.netlify.app
   ```

---

## 🎯 推荐使用GitHub Pages

**优点：**
- ✅ 完全免费
- ✅ 支持自定义域名
- ✅ 全球CDN加速
- ✅ 自动HTTPS

**访问地址示例：**
```
https://yourname.github.io/xiaohongshu-posts/
```

---

## 📱 更新内容

当生成新的爆文后，只需要：

```bash
cd h5
git add .
git commit -m "Update posts"
git push
```

GitHub Pages会自动更新，1-2分钟后生效。

---

## 🔗 自定义域名（可选）

如果想用自己的域名：

1. 在域名DNS设置中添加CNAME记录：
   ```
   xiaohongshu.yourdomain.com → YOUR_USERNAME.github.io
   ```

2. 在GitHub仓库的Settings → Pages中添加自定义域名

3. GitHub会自动配置SSL证书

---

## ⚠️ 注意事项

1. **CSV文件路径**：H5页面需要正确指向CSV文件
2. **CORS问题**：如果遇到跨域问题，需要添加 `.htaccess` 文件
3. **更新频率**：GitHub Pages更新需要1-2分钟

---

## 🚀 一键部署脚本

创建 `deploy.bat` 文件：

```batch
@echo off
echo 正在部署到GitHub Pages...
cd h5
git add .
git commit -m "Update posts - %date% %time%"
git push
echo.
echo ✅ 部署成功！
echo 访问地址：https://YOUR_USERNAME.github.io/xiaohongshu-posts/
echo.
echo 1-2分钟后生效
pause
```

每次生成新爆文后，双击这个脚本即可更新。
