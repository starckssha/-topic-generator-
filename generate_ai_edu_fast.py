#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速生成AI+教育话题页面（跳过图片API，直接使用占位图）
"""
import os
import sys
import glob
import json
import urllib.parse
import requests
from datetime import datetime

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# AI+教育关键词库（优化版）
AI_EDU_KEYWORDS = {
    'AI前沿': ['AI', 'Claude', 'ChatGPT', 'OpenAI', 'GPT', 'LLM', 'LLaMA', 'Gemini', 'artificial intelligence', '机器学习', '深度学习', '人工智能', '智能', 'neural', 'transformer', 'model', 'AI工具', 'AI革命', 'prompt', 'agent', 'copilot'],
    '编程开发': ['code', 'programming', '编程', 'developer', 'API', 'database', 'algorithm', '数据结构', '框架', 'Python', 'JavaScript', 'TypeScript', 'Rust', 'Go', 'Java', 'GitHub', 'Git', '开源', 'open source', 'DevOps', 'Docker', 'LLVM', 'compiler'],
    '学习成长': ['tutorial', 'guide', 'course', 'lesson', '教学', 'training', 'best practice', '最佳实践', '技巧', 'tips', 'how to', 'learn', 'study', 'master', '入门', '精通', '指南', '教程', '实战', 'education', 'school', 'university'],
    '科技产品': ['Apple', 'Google', 'Microsoft', 'Siri', 'iPhone', 'Android', 'app', 'application', 'platform', '工具', 'tool', 'service', 'product', '产品', '发布', 'release', 'launch', 'update', 'Chromium', 'browser'],
    '技术趋势': ['innovation', '创新', 'trend', '趋势', 'future', '未来', 'revolution', '变革', 'breakthrough', '突破', 'research', '研究', 'technology', '科技', 'tech', 'digital', '数字']
}


def parse_topics_from_markdown(content):
    """从Markdown内容解析话题"""
    topics = []
    lines = content.split('\n')

    current_platform = None
    current_topic = None

    for line in lines:
        # 检测平台
        if line.startswith('## 📱'):
            current_platform = line.replace('## 📱', '').strip()

        # 检测话题标题
        elif line.startswith('### '):
            if current_topic:
                topics.append(current_topic)

            # 提取标题
            title = line.replace('###', '').strip()
            # 移除编号
            if '. ' in title:
                title = title.split('. ', 1)[1]

            current_topic = {
                'platform': current_platform or 'Unknown',
                'title': title,
                'heat': 0,
                'url': ''
            }

        # 检测热度
        elif line.strip().startswith('- **热度**') and current_topic:
            parts = line.split(':', 1)
            if len(parts) > 1:
                heat_str = parts[1].strip()
                try:
                    current_topic['heat'] = int(heat_str)
                except:
                    pass

        # 检测链接
        elif line.strip().startswith('- **链接**') and current_topic:
            # 提取URL
            if '](' in line:
                url = line.split('](')[1].rstrip(')')
                current_topic['url'] = url

    # 添加最后一个话题
    if current_topic:
        topics.append(current_topic)

    return topics


def generate_xiaohongshu_content(title):
    """生成小红书文案"""
    title_lower = title.lower()

    if any(kw in title_lower for kw in ['claude', 'chatgpt', 'ai', 'gemini', 'llm']):
        return f"""{title}

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

    elif any(kw in title_lower for kw in ['code', 'programming', '编程', '开发', 'api', 'llvm', 'compiler']):
        return f"""{title}

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
        return f"""{title}

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

    else:
        return f"""{title}

✨ 今天的热点话题

这个内容值得一看👀

💡 核心要点：
• 深度解析
• 专业观点
• 实用价值

📚 持续关注获取更多精彩内容

#热点 #干货 #分享 #知识 #资讯"""


def generate_tags(title):
    """根据标题生成标签"""
    base_tags = ['热点', '干货', '分享']
    title_lower = title.lower()

    if any(kw in title_lower for kw in ['ai', 'chatgpt', '人工智能', 'claude', 'gemini']):
        base_tags.extend(['AI', '人工智能', 'ChatGPT'])
    elif any(kw in title_lower for kw in ['code', 'programming', '编程', '开发']):
        base_tags.extend(['编程', '开发'])
    elif any(kw in title_lower for kw in ['apple', 'google', 'siri']):
        base_tags.extend(['科技', '数码'])
    elif any(kw in title_lower for kw in ['learn', 'tutorial', '学习', '教程']):
        base_tags.extend(['学习', '教程'])

    return base_tags[:5]


def filter_ai_education_topics(topics):
    """筛选AI+教育相关话题"""
    filtered = []

    for topic in topics:
        title_lower = topic['title'].lower()

        # 检查是否包含相关关键词
        for category, keywords in AI_EDU_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    topic['category'] = category
                    filtered.append(topic)
                    break
            else:
                continue
            break

    return filtered


def generate_placeholder_image(title):
    """生成占位图片URL"""
    encoded_title = urllib.parse.quote(title[:30])
    return f"https://placehold.co/600x400/667eea/white?text={encoded_title}&font=roboto"


# 图片生成API配置
IMAGE_API_URL = "https://meye-website.applesay.cn/app-api/meye/draw"
IMAGE_API_AUTH = "Bearer c16617874e424b39af783fd83a751699"


def submit_image_generation(title, max_retries=3):
    """
    提交图片生成请求

    Returns:
        任务ID或None
    """
    headers = {
        'Authorization': IMAGE_API_AUTH,
        'Content-Type': 'application/json'
    }

    prompt = f"小红书配图：{title}，现代简约风格，色彩鲜明"

    data = {
        'appId': 124,
        'type': 'text_to_image',
        'size': 1,
        'input': json.dumps({'prompt': prompt}, ensure_ascii=False)
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(IMAGE_API_URL, headers=headers, json=data, timeout=30)
            result = response.json()

            if result.get('code') == 0 and 'data' in result:
                task_id = result['data'].get('id')
                return task_id
            else:
                print(f"    ⚠️ API返回错误: {result.get('msg', 'Unknown error')}")
                return None

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"    ⚠️ 请求失败，重试 {attempt + 1}/{max_retries}...")
                import time
                time.sleep(2)
            else:
                print(f"    ✗ 提交失败: {e}")
                return None

    return None


def poll_image_result(task_id, max_polls=20, poll_interval=5):
    """
    轮询查询图片生成结果

    Args:
        task_id: 任务ID
        max_polls: 最大轮询次数
        poll_interval: 轮询间隔（秒）

    Returns:
        图片URL或None
    """
    headers = {
        'Authorization': IMAGE_API_AUTH,
        'Content-Type': 'application/json'
    }

    # 尝试多个可能的查询路径
    query_paths = [
        f'/app-api/meye/draw/{task_id}',
        f'/app-api/meye/image/{task_id}',
        f'/app-api/meye/result/{task_id}',
    ]

    for poll in range(max_polls):
        for path in query_paths:
            try:
                url = f"https://meye-website.applesay.cn{path}"
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    result = response.json()

                    # 检查是否返回图片URL
                    if 'data' in result and isinstance(result['data'], dict):
                        # 可能的字段名
                        possible_url_fields = ['imageUrl', 'image', 'url', 'image_url', 'result']

                        for field in possible_url_fields:
                            if field in result['data']:
                                image_url = result['data'][field]
                                if image_url and isinstance(image_url, str) and image_url.startswith('http'):
                                    return image_url

                    # 检查是否直接返回URL
                    if 'data' in result and isinstance(result['data'], str) and result['data'].startswith('http'):
                        return result['data']

            except Exception:
                pass

        # 等待后继续轮询
        import time
        if poll < max_polls - 1:
            time.sleep(poll_interval)

    return None


def batch_generate_images(topics, concurrent_limit=5):
    """
    批量生成图片（排队+轮询）

    Args:
        topics: 话题列表
        concurrent_limit: 并发限制

    Returns:
        更新后的话题列表，包含image_url字段
    """
    import time

    print(f"\n🎨 开始批量生成图片（共 {len(topics)} 个）")
    print(f"⚙️ 并发限制: {concurrent_limit}")
    print(f"⏱️  预计时间: ~{len(topics) * 30}秒\n")

    # 第一阶段：排队提交所有任务
    print("📋 [阶段1/3] 排队提交生图请求...")
    task_queue = []

    for i, topic in enumerate(topics, 1):
        print(f"  [{i}/{len(topics)}] 提交: {topic['title'][:40]}... ", end='', flush=True)

        task_id = submit_image_generation(topic['title'])

        if task_id:
            print(f"✓ (任务ID: {task_id})")
            task_queue.append({
                'topic': topic,
                'task_id': task_id,
                'index': i
            })
        else:
            print("✗ 使用占位图")
            topic['image_url'] = generate_placeholder_image(topic['title'])

        # 避免请求过快
        time.sleep(0.5)

    if not task_queue:
        print("\n⚠️ 没有成功提交任何生图任务")
        return topics

    print(f"\n✓ 成功提交 {len(task_queue)} 个任务")

    # 第二阶段：轮询获取结果
    print(f"\n🔄 [阶段2/3] 轮询获取图片结果...")
    print(f"⏳ 每个任务最多轮询 20 次，间隔 5 秒\n")

    completed = 0
    for item in task_queue:
        topic = item['topic']
        task_id = item['task_id']
        index = item['index']

        print(f"  [{index}/{len(topics)}] 查询任务 {task_id}: ", end='', flush=True)

        image_url = poll_image_result(task_id, max_polls=20, poll_interval=5)

        if image_url:
            print(f"✓\n    URL: {image_url}")
            topic['image_url'] = image_url
        else:
            print("✗ 使用占位图")
            topic['image_url'] = generate_placeholder_image(topic['title'])

        completed += 1

    # 第三阶段：统计
    print(f"\n📊 [阶段3/3] 生图完成统计:")
    api_images = sum(1 for t in topics if not t['image_url'].startswith('https://placehold.co'))
    placeholder_images = len(topics) - api_images

    print(f"  • API生成: {api_images} 张")
    print(f"  • 占位图片: {placeholder_images} 张")

    return topics


def main():
    """主函数"""
    print("="*70)
    print("🤖 AI+教育话题生成器（图片生成版）")
    print("="*70)
    print()

    # 1. 加载话题
    print("[1/4] 加载最新话题...")
    files = glob.glob('output/hot_topics_*.md')
    if not files:
        print("❌ 未找到话题文件")
        return

    latest_file = max(files)
    print(f"📂 读取: {latest_file}")

    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()

    topics = parse_topics_from_markdown(content)
    print(f"✓ 加载了 {len(topics)} 条话题\n")

    # 2. 筛选AI+教育话题
    print("[2/4] 筛选AI+教育话题...")
    filtered_topics = filter_ai_education_topics(topics)
    print(f"✓ 筛选出 {len(filtered_topics)} 条相关话题\n")

    # 显示筛选结果
    print("筛选结果:")
    for i, topic in enumerate(filtered_topics[:15], 1):
        print(f"  {i}. [{topic['category']}] {topic['title'][:50]}")

    if len(filtered_topics) > 15:
        print(f"  ... 还有 {len(filtered_topics) - 15} 个话题")

    # 3. 批量生成图片（排队+轮询）
    filtered_topics = batch_generate_images(filtered_topics, concurrent_limit=5)

    # 4. 生成HTML页面
    print("\n[4/4] 生成HTML页面...")

    topics_json = []
    for topic in filtered_topics:
        # 生成小红书内容和标签
        xiaohongshu_text = generate_xiaohongshu_content(topic['title'])
        tags = generate_tags(topic['title'])

        topics_json.append({
            'platform': topic['platform'],
            'title': topic['title'],
            'text': xiaohongshu_text,
            'heat': topic['heat'],
            'tags': tags,
            'image': topic.get('image_url', generate_placeholder_image(topic['title'])),
            'category': topic['category']
        })

    # 生成HTML（与之前相同）
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

            setTimeout(() => {{ window.location.href = schemes[0]; }}, 1000);
            setTimeout(() => {{ window.open('https://www.xiaohongshu.com', '_blank'); }}, 3000);
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

    output_file = 'hot_ai_education.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML页面已生成: {output_file}")

    print("\n" + "="*70)
    print("🎉 生成完成！")
    print("="*70)
    print(f"\n📊 统计:")
    print(f"  - 原始话题: {len(topics)} 条")
    print(f"  - AI+教育话题: {len(filtered_topics)} 条")
    print(f"\n📄 文件: {output_file}")
    print(f"\n💡 访问方式:")
    print(f"  - 本地: file://{os.path.abspath(output_file)}")
    print(f"  - 服务器: python -m http.server 8000")
    print()


if __name__ == '__main__':
    main()
