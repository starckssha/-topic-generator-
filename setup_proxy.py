"""
配置VPN代理到代码中

使用方法：
1. 找到你VPN软件的代理端口
2. 运行此脚本自动配置
"""

import os
import sys

# 请修改这里的端口号
# 常见VPN软件的默认端口：
# - Clash/ClashX: 7890
# - V2rayN: 10808
# - Shadowsocks: 1080
# - 其他: 请查看你的VPN软件设置

PROXY_PORT = 7890  # <- 请修改为你的VPN代理端口

def check_port(port):
    """检查端口是否可用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def setup_proxy_in_code(port):
    """在base_fetcher.py中配置代理"""
    
    proxy_code = f'''
    def _setup_session(self):
        """配置session"""
        # 随机选择User-Agent
        user_agent = random.choice(self.USER_AGENTS)
        
        # 配置代理
        proxies = {{
            'http': 'http://127.0.0.1:{port}',
            'https': 'http://127.0.0.1:{port}',
        }}
        
        self.session = requests.Session()
        self.session.proxies.update(proxies)
        self.session.headers.update({{
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }})
'''
    
    return proxy_code

# 主程序
print("=" * 60)
print("VPN代理配置工具")
print("=" * 60)
print()
print(f"设置的代理端口: {PROXY_PORT}")
print()

# 检查端口
if check_port(PROXY_PORT):
    print(f"[*] 端口 {PROXY_PORT} 正在监听")
else:
    print(f"[!] 端口 {PROXY_PORT} 未被监听")
    print()
    print("请:")
    print("1. 打开你的VPN软件")
    print("2. 查找'设置'或'Preferences'")
    print("3. 找到'本地代理端口'或'Local Proxy Port'")
    print("4. 修改本文件的 PROXY_PORT 变量")
    print("5. 重新运行此脚本")
    sys.exit(1)

print()
print("[*] 正在生成配置代码...")
print()
print("请在 src/base_fetcher.py 的 _setup_session 方法中使用以下代码:")
print()
print("=" * 60)
print(setup_proxy_in_code(PROXY_PORT))
print("=" * 60)
print()
print("配置完成后，运行: python main.py")
