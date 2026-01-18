# Clash 设置指南 - 解决SSL问题

## 问题诊断

所有连接都失败，包括curl。这说明Clash可能需要调整设置。

## 请检查以下Clash设置

### 1. 打开Clash设置

- 系统托盘找到Clash图标
- 右键 → 设置

### 2. 检查以下配置

#### ✅ 允许局域网连接
- **选项**: "允许局域网连接" 或 "Allow LAN"
- **必须勾选**: ✓

#### ✅ 局域网地址
- **设置**: `127.0.0.1` 或 `0.0.0.0`
- **端口**: `7897`

#### ✅ 代理模式
- **选项**: "HTTP代理" 或 "Mixed Port"
- **端口**: 确认是 7897

#### ✅ TLS设置
- **选项**: 找到"TLS"或"安全"设置
- **尝试**: 
  - 启用 "允许不安全"
  - 或 "Skip Cert Verify"
  - 或将TLS版本设置为 1.2 或 1.3

### 3. 重新启动Clash

修改设置后：
1. 停止 Clash
2. 重新启动 Clash
3. 确认端口 7897 在监听

### 4. 验证Clash工作

打开浏览器，访问：https://hacker-news.firebaseio.com

如果能访问，说明Clash正常。

### 5. 测试代理

```bash
curl -x http://127.0.0.1:7897 https://www.google.com -I
```

应该返回 `200 OK` 或 `302 Redirect`

## 如果还是不行

### 选项A: 切换到TUN模式

在Clash设置中：
1. 找到"模式"或"Mode"
2. 切换到 "TUN" 或 "tun"
3. 重启Clash
4. 移除代码中的代理配置

### 选项B: 使用系统代理

1. 在Clash中启用"系统代理"
2. 修改Python代码，移除显式代理设置

### 选项C: 更新Clash

使用最新版Clash Verge Rev：
- https://github.com/Clash-verge-rev/clash-verge-rev

新版本可能修复了OpenSSL 3.4兼容性

## 快速检查命令

```bash
# 检查端口是否监听
netstat -ano | findstr "7897"

# 测试代理
curl -x http://127.0.0.1:7897 https://www.baidu.com -I

# 检查Clash进程
tasklist | findstr "clash"
```

## 配置完成后

重新运行测试：
```bash
cd D:\Projects\ClaudeCode\topicgenerater
python main.py
```

## 需要帮助？

请告诉我：
1. Clash的完整名称（Clash for Windows / ClashX / Clash Verge等）
2. "允许局域网连接"是否勾选
3. 当前使用什么模式（HTTP/SOCKS5/TUN）

我会帮你进一步配置！
