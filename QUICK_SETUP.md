# VPN代理快速配置指南

## 步骤1：找到你的VPN代理端口

### 不同VPN软件查看方法：

**Clash/ClashX:**
1. 打开Clash
2. 点击"设置"或"Settings"
3. 查看"端口(Port)"或"Port"
4. 通常是：7890 或 7891

**V2rayN:**
1. 打开V2rayN
2. 点击"参数设置"
3. 查看"本地监听端口"
4. 通常是：10808

**Shadowsocks:**
1. 打开Shadowsocks
2. 查看选项设置
3. 通常是：1080

**其他VPN:**
- 查看软件的"设置"、"Preferences"、"配置"
- 找到"Local Proxy"、"本地代理"、"HTTP Proxy"
- 记下端口号

## 步骤2：配置到代码中

### 方法A：使用配置文件（推荐）

创建 `config_with_proxy.py`:

```python
CONFIG = {
    'enabled_platforms': ['hackernews'],
    'hackernews_count': 20,
    'output_dir': 'output',
    'timeout': 15,
    
    # 添加你的代理端口
    'proxy_port': 7890,  # 修改为你的端口
}
```

### 方法B：直接修改base_fetcher.py

编辑 `src/base_fetcher.py`，找到 `_setup_session` 方法，添加：

```python
def _setup_session(self):
    # 原有代码...
    
    # 在最后添加这几行：
    proxy_port = 7890  # 修改为你的端口
    proxies = {
        'http': f'http://127.0.0.1:{proxy_port}',
        'https': f'http://127.0.0.1:{proxy_port}',
    }
    self.session.proxies.update(proxies)
```

## 步骤3：测试

运行程序测试：
```bash
python main.py
```

## 如果还是失败

### 选项1：使用系统代理
有些VPN使用系统代理，Python会自动使用

### 选项2：尝试socks5代理
如果VPN使用socks5，需要安装：`pip install requests[socks]`

### 选项3：使用TUN模式
有些VPN的TUN模式不需要配置代理，直接生效

## 验证VPN工作正常

在浏览器中访问：https://hackernews.firebaseio.com
如果能访问，说明VPN正常。
