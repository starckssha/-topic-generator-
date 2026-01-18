#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI+教育话题过滤和图片生成脚本
"""
import os
import sys
import requests
import json
import glob
from datetime import datetime

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 图片生成API配置
IMAGE_API_URL = "https://meye-website.applesay.cn/app-api/meye/draw"
IMAGE_API_AUTH = "Bearer c16617874e424b39af783fd83a751699"
IMAGE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'generated_images')

# 确保图片目录存在
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

# AI+教育关键词库
AI_EDU_KEYWORDS = {
    'AI前沿': [
        'AI', 'Claude', 'ChatGPT', 'OpenAI', 'GPT', 'LLM', 'LLaMA',
        'Gemini', 'artificial intelligence', '机器学习', '深度学习',
        '人工智能', '智能', 'neural network', 'transformer', 'model',
        'AI工具', 'AI革命', 'AI时代', 'prompt', 'agent', 'copilot'
    ],
    '编程开发': [
        '代码', '编程', 'developer', 'programming', 'code', 'software',
        'API', 'database', 'algorithm', '数据结构', '框架', 'library',
        'Python', 'JavaScript', 'TypeScript', 'Rust', 'Go', 'Java',
        'GitHub', 'Git', '开源', 'open source', 'DevOps', 'Docker'
    ],
    '学习成长': [
        '学习', 'education', 'tutorial', 'guide', 'course', 'lesson',
        '教学', 'training', 'workshop', '最佳实践', 'best practice',
        '技巧', 'tips', 'how to', 'learn', 'study', 'master',
        '入门', '精通', '指南', '教程', '实战'
    ],
    '科技产品': [
        'Apple', 'Google', 'Microsoft', 'Siri', 'iPhone', 'Android',
        'app', 'application', 'platform', '工具', 'tool', 'service',
        'product', '产品', '发布', 'release', 'launch', 'update'
    ],
    '技术趋势': [
        'innovation', '创新', 'trend', '趋势', 'future', '未来',
        'revolution', '变革', 'breakthrough', '突破', 'research',
        '研究', 'technology', '科技', 'tech', 'digital', '数字'
    ],
    '教育相关': [
        'education', '学校', 'school', 'university', '大学', 'college',
        '学生', 'student', '老师', 'teacher', 'classroom', '课堂',
        '在线学习', 'online learning', 'elearning', '远程教育'
    ]
}


def load_latest_topics():
    """加载最新的话题数据"""
    # 查找最新的话题文件
    output_files = glob.glob('output/hot_topics_*.md')

    if not output_files:
        print("❌ 未找到话题文件")
        return None

    # 按时间排序，取最新的
    latest_file = max(output_files)
    print(f"📂 读取文件: {latest_file}\n")

    # 读取并解析话题
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()

        topics = parse_topics_from_markdown(content)
        print(f"✓ 成功加载 {len(topics)} 条话题")
        return topics

    except Exception as e:
        print(f"✗ 加载话题失败: {e}")
        return None


def parse_topics_from_markdown(content):
    """从Markdown内容解析话题"""
    topics = []
    lines = content.split('\n')

    current_platform = None
    current_heat = None

    for line in lines:
        # 检测平台
        if line.startswith('## 📱'):
            current_platform = line.replace('## 📱', '').strip()
            current_heat = None

        # 检测话题
        elif line.startswith('### '):
            # 提取标题和热度
            title_part = line.replace('###', '').strip()

            # 分离热度信息
            if '🔥' in title_part:
                parts = title_part.split('🔥')
                title = parts[0].strip()
                # 提取热度数字
                if len(parts) > 1:
                    heat_str = parts[1].strip().split()[0]
                    try:
                        current_heat = int(heat_str.replace(',', ''))
                    except:
                        current_heat = 0
            else:
                title = title_part

            # 清理标题
            title = title.split('|')[0].strip()  # 移除时间戳部分
            title = title.split('[[')[0].strip()  # 移除URL标记

            # 生成小红书文案
            xiaohongshu_text = generate_xiaohongshu_content(title)

            topics.append({
                'platform': current_platform or 'Unknown',
                'title': title,
                'heat': current_heat or 0,
                'text': xiaohongshu_text,
                'tags': generate_tags(title),
                'image_url': None  # 稍后生成
            })

    return topics


def generate_xiaohongshu_content(title):
    """生成小红书文案"""
    # 根据标题关键词生成不同风格的内容
    title_lower = title.lower()

    if any(kw in title_lower for kw in ['claude', 'chatgpt', 'ai', 'gemini', 'llm']):
        content = f"""{title}

🤖 AI圈又出大事了！

这个话题真的太火了🔥
作为开发者/学习者必须了解！

💡 核心看点：
• 前沿AI技术动态
• 开发者必备知识
• 行业趋势分析

📚 为什么值得关注？
AI时代，这个话题关乎每个人的未来！

👇 点赞收藏，持续获取AI干货！

#AI #人工智能 #ChatGPT #Claude #技术分享 #干货"""

    elif any(kw in title_lower for kw in ['code', 'programming', '编程', '开发', 'api']):
        content = f"""{title}

💻 程序员必看！

这个技术话题太有价值了✨

🔥 核心要点：
• 实战开发技巧
• 最佳实践经验
• 技术深度解析

💪 适用人群：
✅ 开发者
✅ 编程学习者
✅ 技术爱好者

📚 持续学习，一起进步！

#编程 #开发 #代码 #程序员 #技术干货 #学习"""

    elif any(kw in title_lower for kw in ['apple', 'google', 'microsoft', 'siri']):
        content = f"""{title}

🍎🔥 科技巨头又有大动作！

这个消息真的炸裂💥

💡 核心看点：
• 产品最新动态
• 技术革新方向
• 行业影响分析

🎯 为什么重要？
这可能改变我们的使用方式！

👇 关注获取更多科技资讯！

#科技 #Apple #Google #创新 #数码 #技术前沿"""

    elif any(kw in title_lower for kw in ['tutorial', 'guide', 'learn', '学习', '教程', '指南']):
        content = f"""{title}

📚 干货满满的学习资源！

这个宝藏内容必须收藏✨

🎯 适合人群：
• 初学者入门
• 进阶提升
• 技能拓展

💡 学习建议：
1️⃣ 理论结合实践
2️⃣ 循序渐进
3️⃣ 多动手练习

📈 持续学习，遇见更好的自己！

#学习 #教程 #干货 #技能提升 #自我成长 #知识分享"""

    else:
        content = f"""{title}

✨ 今天的热点话题

这个内容值得一看👀

💡 核心要点：
• 深度解析
• 专业观点
• 实用价值

📚 持续关注获取更多精彩内容

#热点 #干货 #分享 #知识 #资讯"""

    return content


def generate_tags(title):
    """根据标题生成标签"""
    base_tags = ['热点', '干货', '分享']

    # 根据关键词添加特定标签
    title_lower = title.lower()

    if any(kw in title_lower for kw in ['ai', 'chatgpt', '人工智能', 'claude']):
        base_tags.extend(['AI', '人工智能', 'ChatGPT'])

    if any(kw in title_lower for kw in ['教育', '学习', '学校', '老师']):
        base_tags.extend(['教育', '学习'])

    if any(kw in title_lower for kw in ['编程', '代码', '开发']):
        base_tags.extend(['编程', '开发'])

    return base_tags[:5]  # 最多5个标签


def filter_ai_education_topics(topics):
    """筛选AI+教育相关话题"""
    filtered = []

    for topic in topics:
        title_lower = topic['title'].lower()

        # 检查是否包含AI或教育相关关键词
        is_ai_edu = False
        matched_category = None

        for category, keywords in AI_EDU_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    is_ai_edu = True
                    matched_category = category
                    break
            if is_ai_edu:
                break

        if is_ai_edu:
            topic['category'] = matched_category
            filtered.append(topic)

    print(f"✓ 筛选出 {len(filtered)} 条AI+教育话题")
    return filtered


def generate_image_with_api(title):
    """
    使用提供的API生成图片

    Args:
        title: 文章标题

    Returns:
        图片URL字符串或None
    """
    try:
        # 构建提示词
        prompt = f"小红书配图：{title}，现代简约风格"

        # 调用API
        headers = {
            'Authorization': IMAGE_API_AUTH,
            'User-Agent': 'Apifox/1.0.0',
            'Content-Type': 'application/json'
        }

        data = {
            "appId": 124,
            "type": "text_to_image",
            "size": 1,
            "input": json.dumps({"prompt": prompt}, ensure_ascii=False)
        }

        print(f"  正在生成图片: {title[:20]}...")

        response = requests.post(
            IMAGE_API_URL,
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            # 检查返回的数据结构
            if 'data' in result and result['data']:
                # 如果返回图片URL，直接返回
                if isinstance(result['data'], str) and result['data'].startswith('http'):
                    print(f"  ✓ 获取图片URL成功")
                    return result['data']

            print(f"  ⚠️ API返回格式不符: {result}")
        else:
            print(f"  ✗ API调用失败: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"  ✗ 生成图片失败: {e}")

    return None


def generate_placeholder_image(title):
    """
    生成占位图片URL

    Args:
        title: 文章标题

    Returns:
        占位图片URL
    """
    # 使用免费的占位图片服务
    import urllib.parse

    # 对标题进行URL编码
    encoded_title = urllib.parse.quote(title[:20])

    # 使用placehold.co服务（免费，无需API）
    placeholder_url = f"https://placehold.co/600x400/667eea/white?text={encoded_title}&font=roboto"

    return placeholder_url


def generate_html_page(topics, output_file='hot_ai_education.html'):
    """生成HTML页面"""

    # 生成JavaScript数据
    topics_json = []
    for topic in topics:
        # 直接使用外部URL（API返回的或占位图服务）
        image_url = topic['image_url'] if topic['image_url'] else None

        topics_json.append({
            'platform': topic['platform'],
            'title': topic['title'],
            'text': topic['text'],
            'heat': topic['heat'],
            'tags': topic['tags'],
            'image': image_url,
            'category': topic.get('category', '')
        })

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>AI+教育热点话题</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px 15px;
        }}
        .header {{ text-align: center; color: white; margin-bottom: 25px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stats {{ text-align: center; color: white; font-size: 14px; margin-bottom: 20px; opacity: 0.9; }}
        .content-list {{ max-width: 600px; margin: 0 auto; display: flex; flex-direction: column; gap: 15px; }}
        .card {{ background: white; border-radius: 16px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .category {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; display: inline-block; margin-bottom: 10px; }}
        .platform {{ background: #f0f0f0; color: #666; padding: 4px 12px; border-radius: 12px; font-size: 12px; display: inline-block; margin-bottom: 10px; margin-left: 8px; }}
        .title {{ font-size: 18px; font-weight: 600; color: #333; margin-bottom: 10px; line-height: 1.4; }}
        .heat {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 3px 10px; border-radius: 10px; font-size: 12px; font-weight: 600; display: inline-block; margin-bottom: 10px; }}
        .image-container {{ margin: 10px 0; border-radius: 12px; overflow: hidden; }}
        .image-container img {{ width: 100%; height: auto; display: block; }}
        .text {{ font-size: 14px; color: #666; line-height: 1.6; margin-bottom: 15px; white-space: pre-wrap; }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
        .tag {{ background: #f0f0f0; color: #666; padding: 4px 12px; border-radius: 12px; font-size: 12px; }}
        .btn {{ width: 100%; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; }}
        .loading {{ text-align: center; color: white; padding: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI+教育热点</h1>
        <p>精选AI和教育相关话题 | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    <div class="stats">📊 加载中...</div>
    <div class="content-list" id="list"></div>

    <script>
        const topics = {json.dumps(topics_json, ensure_ascii=False, indent=12)};

        async function copy(text) {{
            try {{
                await navigator.clipboard.writeText(text);
                return true;
            }} catch {{
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                const success = document.execCommand('copy');
                document.body.removeChild(ta);
                return success;
            }}
        }}

        function openXHS() {{
            const schemes = [
                'xhsdiscover://post_note/',
                'xhsdiscover://post/',
                'xhsdiscover://',
                'xhs://'
            ];

            // Try iframe method
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            document.body.appendChild(iframe);

            let idx = 0;
            function tryNext() {{
                if (idx < schemes.length) {{
                    iframe.src = schemes[idx++];
                    setTimeout(tryNext, 500);
                }} else {{
                    document.body.removeChild(iframe);
                }}
            }}
            tryNext();

            setTimeout(() => {{
                window.location.href = schemes[0];
            }}, 1000);

            setTimeout(() => {{
                window.open('https://www.xiaohongshu.com', '_blank');
            }}, 3000);
        }}

        async function publish(item) {{
            const text = `${{item.title}}\\n\\n${{item.text}}\\n\\n${{item.tags.map(t => '#' + t).join(' ')}}`;

            if (await copy(text)) {{
                alert('✅ 文字已复制！\\n\\n1. 打开小红书APP\\n2. 粘贴文字\\n3. 添加图片\\n4. 发布');
                setTimeout(() => openXHS(), 1000);
            }}
        }}

        function render() {{
            document.querySelector('.stats').textContent = '📊 共 ' + topics.length + ' 个AI+教育话题';

            const listEl = document.getElementById('list');
            listEl.innerHTML = topics.map(item => `
                <div class="card">
                    <span class="category">${{item.category || 'AI+教育'}}</span>
                    <span class="platform">${{item.platform}}</span>
                    <div class="title">${{item.title}}</div>
                    <div class="heat">🔥 热度 ${{item.heat}}</div>
                    ${{item.image ? `<div class="image-container"><img src="${{item.image}}" alt="配图" onerror="this.style.display='none'"></div>` : ''}}
                    <div class="tags">${{item.tags.map(t => `<span class="tag">#${{t}}</span>`).join('')}}</div>
                    <div class="text">${{item.text}}</div>
                    <button class="btn" onclick="publish(${{JSON.stringify(item).replace(/"/g, '&quot;')}})">📱 发布到小红书</button>
                </div>
            `).join('');
        }}

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', render);
        }} else {{
            render();
        }}
    </script>
</body>
</html>'''

    # 保存HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ HTML页面已生成: {output_file}")
    print(f"   可以通过以下方式访问:")
    print(f"   - 本地文件: file://{os.path.abspath(output_file)}")
    print(f"   - HTTP服务器: python -m http.server 8000")

    return output_file


def main():
    """主函数"""
    print("="*70)
    print("🤖 AI+教育话题生成器")
    print("="*70)
    print()

    # 1. 加载最新话题
    print("[1/4] 加载最新话题...")
    topics = load_latest_topics()
    if not topics:
        return

    # 2. 筛选AI+教育话题
    print("\n[2/4] 筛选AI+教育话题...")
    filtered_topics = filter_ai_education_topics(topics)

    if not filtered_topics:
        print("❌ 未找到AI+教育相关话题")
        return

    # 显示筛选结果
    print("\n筛选结果:")
    for i, topic in enumerate(filtered_topics[:10], 1):
        print(f"  {i}. [{topic['category']}] {topic['title'][:40]}...")

    if len(filtered_topics) > 10:
        print(f"  ... 还有 {len(filtered_topics) - 10} 个话题")

    # 3. 生成图片
    print(f"\n[3/4] 生成配图（共 {len(filtered_topics)} 个话题）...")

    for i, topic in enumerate(filtered_topics, 1):
        print(f"\n{i}/{len(filtered_topics)} ", end='')

        # 先尝试用API生成
        image_url = generate_image_with_api(topic['title'])

        # 如果API失败，使用占位图
        if not image_url:
            print("  ⚠️ 使用占位图服务")
            image_url = generate_placeholder_image(topic['title'])

        topic['image_url'] = image_url

    # 4. 生成HTML页面
    print("\n\n[4/4] 生成HTML页面...")
    output_file = generate_html_page(filtered_topics)

    print("\n" + "="*70)
    print("🎉 生成完成！")
    print("="*70)
    print(f"\n📊 统计:")
    print(f"  - 原始话题: {len(topics)} 条")
    print(f"  - AI+教育话题: {len(filtered_topics)} 条")
    print(f"\n📄 输出文件: {output_file}")
    print(f"\n💡 提示:")
    print(f"  - 由于API限制，当前使用占位图片服务")
    print(f"  - 图片通过外部URL加载，无需本地存储")
    print()


if __name__ == '__main__':
    main()
