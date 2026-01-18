import requests
import sys

# 只测试实际存在的端口
test_ports = [7892, 7897, 7898, 7899]

print("Testing VPN proxy ports...\n")

working_ports = []

for port in test_ports:
    proxy_url = f"http://127.0.0.1:{port}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }
    
    try:
        print(f"[*] Testing port {port}...", end=' ')
        
        # 使用更简单的测试URL
        response = requests.get(
            'https://www.baidu.com',  # 使用国内网站测试
            proxies=proxies, 
            timeout=3
        )
        
        if response.status_code == 200:
            print(f"OK! Working!")
            working_ports.append(port)
        else:
            print(f"Status: {response.status_code}")
            
    except Exception as e:
        print(f"Failed")

print()
if working_ports:
    print(f"Working ports found: {working_ports}")
    print(f"\nUse this in config:")
    print(f"PROXY_PORT = {working_ports[0]}")
else:
    print("No working proxy ports found")
    print("\nPlease check your VPN software settings")
    print("Look for 'Local Proxy Port' or similar")
