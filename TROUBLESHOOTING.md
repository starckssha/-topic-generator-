# 网络连接问题解决方案

## 问题诊断

当前错误：`SSL: UNEXPECTED_EOF_WHILE_READING`

这是SSL/TLS握手失败，可能的原因：
1. VPN未正确配置
2. 系统代理设置冲突
3. Python SSL库问题
4. 防火墙阻止

## 解决方案

### 方案1：验证VPN连接

```bash
# 测试VPN是否工作
curl https://www.google.com

# 或者
ping www.google.com
```

### 方案2：配置代理

如果VPN使用代理，编辑 `src/base_fetcher.py`：

```python
def _setup_session(self):
    # 添加代理配置
    proxies = {
        'http': 'http://127.0.0.1:端口号',
        'https': 'http://127.0.0.1:端口号',
    }
    self.session.proxies.update(proxies)
    
    # 其余配置...
```

### 方案3：使用测试数据模式

创建一个测试版本，使用本地数据：

```bash
python main_test.py  # 使用模拟数据
```

### 方案4：禁用SSL验证（不推荐）

仅用于测试，编辑 `src/base_fetcher.py`：

```python
response = requests.get(url, verify=False, ...)
```

### 方案5：使用国内平台

编辑 `config.py`，只使用国内平台：

```python
'enabled_platforms': [
    'toutiao',   # 今日头条
    'bilibili',  # B站
]
```

## 推荐步骤

1. **确认VPN状态**
   - 检查VPN是否已连接
   - 尝试在浏览器访问 https://hackernews.firebaseio.com

2. **配置系统代理**
   - 如果VPN需要代理，配置系统代理
   - 或在代码中配置代理

3. **使用国内平台测试**
   - 修改配置只使用今日头条、B站
   - 这些平台在国内网络更稳定

4. **联系VPN提供商**
   - 如果问题持续，可能是VPN软件问题
   - 尝试重启VPN或更换节点
