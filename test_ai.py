"""测试AI服务"""
import sys
import io

# 设置编码
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

from src.services.ai_service import SyncAIService

def test_ai():
    service = SyncAIService()

    print('测试DeepSeek API连接...\n')

    try:
        content = service.generate_content_for_topic(
            topic_title='ChatGPT在教育中的应用',
            platform='Hacker News',
            category='AI变革',
            style='写一篇小红书震撼型内容',
            title_type='震撼型'
        )
        print(f'✓ 生成成功！')
        print(f'内容长度: {len(content)} 字符\n')
        print('内容预览:')
        print('=' * 80)
        print(content[:500])
        print('=' * 80)
    except Exception as e:
        print(f'✗ 生成失败: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_ai()
