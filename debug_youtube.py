"""
YouTube调试脚本 - 测试YouTube数据获取
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.fetchers.youtube_fetcher import YouTubeFetcher

def main():
    print("=" * 70)
    print("YouTube 调试工具")
    print("=" * 70)

    # 创建fetcher
    fetcher = YouTubeFetcher(category='tech')

    print("\n[*] 正在获取YouTube页面...")
    url = "https://www.youtube.com/feed/trending?gl=US&hl=en"
    html = fetcher._get_html(url, referer='https://www.youtube.com')

    if not html:
        print("❌ 无法获取YouTube页面")
        return

    print(f"✓ 成功获取HTML内容，长度: {len(html)} 字符")

    # 保存HTML用于分析
    with open('debug_youtube.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ HTML已保存到 debug_youtube.html")

    # 查找关键模式
    import re

    patterns = [
        ('ytInitialData (var)', r'var ytInitialData = ({.+?});'),
        ('ytInitialData (window)', r'window\[["\']ytInitialData["\']\] = ({.+?});'),
        ('videoId', r'"videoId":"([^"]+)"'),
        ('title (runs)', r'"title":\s*{\s*"runs":\s*\[([^\]]+)\]'),
    ]

    print("\n[*] 搜索关键模式...")
    for name, pattern in patterns:
        matches = re.findall(pattern, html[:50000])  # 只看前50KB
        print(f"  {name}: 找到 {len(matches)} 个匹配")
        if matches and len(matches) <= 3:
            for i, match in enumerate(matches[:3]):
                print(f"    [{i+1}] {str(match)[:100]}...")

    # 尝试使用BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有a标签
        links = soup.find_all('a', href=True)
        video_links = [l for l in links if '/watch?v=' in l.get('href', '')]
        print(f"\n[*] BeautifulSoup分析:")
        print(f"  总链接数: {len(links)}")
        print(f"  视频链接数: {len(video_links)}")

        if video_links:
            print(f"\n  前5个视频链接:")
            for i, link in enumerate(video_links[:5]):
                title = link.get('title', '无标题')
                href = link.get('href', '')
                print(f"    [{i+1}] {title[:50]}")
                print(f"        {href[:80]}")

    except ImportError:
        print("\n[*] BeautifulSoup未安装，跳过HTML解析")

    # 正常fetch
    print("\n[*] 使用标准fetch方法...")
    topics = fetcher.fetch(count=20)
    print(f"✓ 获取到 {len(topics)} 条话题")

    if topics:
        print("\n前3条话题:")
        for topic in topics[:3]:
            print(f"  {topic['rank']}. {topic['title']}")
    else:
        print("❌ 未能获取到话题")

if __name__ == '__main__':
    main()
