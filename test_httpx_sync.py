import httpx
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("测试 httpx 同步客户端")
print("=" * 60)
print()

# 配置代理和超时
proxy = "http://127.0.0.1:7897"
timeout = 10.0

# 尝试不同的SSL配置
configs = [
    {"verify": False, "timeout": timeout},
    {"verify": False, "timeout": timeout, "http2": True},
]

for i, config in enumerate(configs, 1):
    try:
        print(f"[*] 尝试配置 {i}...")
        
        client = httpx.Client(
            proxy=proxy,
            **config
        )
        
        response = client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        
        if response.status_code == 200:
            story_ids = response.json()[:5]
            print(f"✓ 成功！获取 {len(story_ids)} 个故事ID")
            
            # 获取第一个故事
            story = client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_ids[0]}.json").json()
            print(f"✓ 标题: {story.get('title', 'N/A')}")
            print(f"✓ httpx 可以工作！")
            print()
            print("正在更新代码使用 httpx...")
            break
        else:
            print(f"状态码: {response.status_code}")
            
    except Exception as e:
        print(f"失败: {str(e)[:50]}")
    
    print()

print("=" * 60)
