import requests
import socket

# Clash常见端口
ports = [7890, 7891, 7892, 7893, 7897, 7898, 7899]

print("=" * 60)
print("正在查找 Clash 代理端口...")
print("=" * 60)
print()

# 先检查哪些端口在监听
listening_ports = []
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        listening_ports.append(port)
        print(f"[*] 端口 {port} 正在监听")

if not listening_ports:
    print("\n未找到Clash端口")
    print("\n请手动检查 Clash 设置：")
    print("1. 打开 Clash")
    print("2. 点击 '设置' 或 'Settings'")
    print("3. 查看 '端口' 或 'Port'")
    print("4. 记下端口号")
else:
    print(f"\n找到 {len(listening_ports)} 个监听端口: {listening_ports}")
    print()
    print("正在测试哪个端口可以工作...")
    
    for port in listening_ports:
        try:
            print(f"[*] 测试端口 {port}...", end=' ')
            proxies = {
                'http': f'http://127.0.0.1:{port}',
                'https': f'http://127.0.0.1:{port}',
            }
            
            # 使用百度测试
            response = requests.get(
                'https://www.baidu.com',
                proxies=proxies,
                timeout=3
            )
            
            if response.status_code == 200:
                print(f"✓ 成功！")
                print(f"\n找到正确的端口: {port}")
                print(f"\n请在 src/base_fetcher.py 中设置:")
                print(f"PROXY_PORT = {port}")
                break
            else:
                print(f"状态码: {response.status_code}")
                
        except Exception as e:
            print(f"失败")

print()
print("=" * 60)
