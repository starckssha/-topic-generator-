import sys

print("检查是否安装了 SOCKS5 支持...")
try:
    import requests
    import urllib3
    print("requests 已安装")
    
    # 尝试安装 PySocks
    try:
        import socks
        print("PySocks 已安装")
    except ImportError:
        print("\n正在安装 PySocks...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PySocks', '-q'])
        print("PySocks 安装完成")
        import socks
    
    print("\n现在测试 SOCKS5 代理...")
    
    # 测试端口
    ports = [7891, 7892, 7897, 7898, 7899]
    
    for port in ports:
        try:
            print(f"[*] 测试 SOCKS5 端口 {port}...", end=' ')
            
            proxies = {
                'http': f'socks5://127.0.0.1:{port}',
                'https': f'socks5://127.0.0.1:{port}',
            }
            
            response = requests.get(
                'https://www.baidu.com',
                proxies=proxies,
                timeout=3
            )
            
            if response.status_code == 200:
                print(f"✓ 成功！")
                print(f"\n找到 SOCKS5 端口: {port}")
                print(f"\n需要配置 SOCKS5，请查看: SOCKS5_SETUP.md")
                break
            else:
                print(f"状态码: {response.status_code}")
                
        except Exception as e:
            print(f"失败: {str(e)[:30]}")
    
except Exception as e:
    print(f"错误: {e}")
