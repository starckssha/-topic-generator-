"""
YouTube API 测试脚本
"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_key():
    """测试API密钥是否有效"""
    print("=" * 70)
    print("YouTube API 测试工具")
    print("=" * 70)

    # 检查API密钥
    api_key = os.getenv('YOUTUBE_API_KEY')

    if not api_key:
        print("\n❌ 未找到YouTube API密钥")
        print("\n请设置环境变量 YOUTUBE_API_KEY：")
        print("  Windows (PowerShell): $env:YOUTUBE_API_KEY='你的密钥'")
        print("  Windows (CMD): set YOUTUBE_API_KEY=你的密钥")
        print("  Linux/Mac: export YOUTUBE_API_KEY='你的密钥'")
        print("\n或者参考文档：docs/YOUTUBE_API_SETUP.md")
        return False

    print(f"\n✓ 找到API密钥: {api_key[:10]}...{api_key[-4:]}")

    # 测试API请求
    print("\n[*] 正在测试API连接...")

    import requests

    # 简单测试：获取一个视频的信息
    test_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet',
        'id': 'dQw4w9WgXcQ',  # Rick Roll视频，用于测试
        'key': api_key
    }

    try:
        response = requests.get(test_url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                video_title = data['items'][0]['snippet']['title']
                print(f"✓ API连接成功！")
                print(f"  测试视频: {video_title}")
                return True
            else:
                print("❌ API返回了空数据")
                return False

        elif response.status_code == 403:
            error_data = response.json()
            error_reason = error_data.get('error', {}).get('errors', [{}])[0].get('reason', 'Unknown')
            print(f"❌ API访问被拒绝")
            print(f"  原因: {error_reason}")

            if error_reason == 'quotaExceeded':
                print("\n💡 配额已用完，请明天再试或增加配额")
            elif error_reason == 'keyInvalid':
                print("\n💡 API密钥无效，请检查密钥是否正确")
            elif error_reason == 'forbidden':
                print("\n💡 YouTube Data API未启用")
                print("  请访问: https://console.cloud.google.com/")
                print("  并启用YouTube Data API v3")

            return False

        else:
            print(f"❌ API请求失败 (HTTP {response.status_code})")
            print(f"  响应: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ 请求出错: {e}")
        return False


def test_fetch_videos():
    """测试获取热门视频"""
    print("\n" + "=" * 70)
    print("测试获取YouTube热门视频")
    print("=" * 70)

    from src.fetchers.youtube_api_fetcher import YouTubeAPIFetcher

    # 创建fetcher实例
    fetcher = YouTubeAPIFetcher(category='tech')

    print("\n[*] 正在获取科技类热门视频...")
    videos = fetcher.fetch(count=5)

    if videos:
        print(f"\n✓ 成功获取 {len(videos)} 条视频：\n")
        for video in videos:
            print(f"  {video['rank']}. {video['title'][:60]}...")
            print(f"     观看: {video['hot_value']:,} 次")
            print(f"     链接: {video['url']}")
            print()
        return True
    else:
        print("❌ 未能获取到视频")
        return False


def main():
    """主函数"""
    print("\n🚀 开始测试YouTube API配置\n")

    # 测试API密钥
    api_valid = test_api_key()

    if not api_valid:
        print("\n" + "=" * 70)
        print("❌ API密钥测试失败")
        print("=" * 70)
        print("\n请解决上述问题后重新运行测试")
        return 1

    # 测试获取视频
    videos_ok = test_fetch_videos()

    print("=" * 70)
    if videos_ok:
        print("✅ 所有测试通过！YouTube API配置成功")
        print("\n现在可以运行主程序：")
        print("  python main.py")
    else:
        print("⚠️  API密钥有效，但获取视频失败")
        print("\n可能的原因：")
        print("  1. 配额已用完")
        print("  2. 网络连接问题")
        print("  3. API服务暂时不可用")
    print("=" * 70)

    return 0 if videos_ok else 1


if __name__ == '__main__':
    sys.exit(main())
