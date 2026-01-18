#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书爆文生成器 - 海外教育+AI专题
从网络热点话题生成小红书爆款内容
"""
import os
import sys
import re
from datetime import datetime
from topic_tracker import TopicTracker

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class XiaohongshuGenerator:
    """小红书爆文生成器 - 海外教育AI专题"""

    # 海外教育+AI关键词库
    PARENT_KEYWORDS = {
        'AI变革': [
            'AI教育', 'ChatGPT', 'OpenAI', 'AI老师', 'AI辅助教学',
            '智能教育', '教育科技', 'EdTech', '人工智能教育',
            'AI改变教育', '教育AI化', 'AI革命', '技术变革',
            '机器学习教育', 'AI课堂', '智能tutor',
            # 英文关键词
            'AI', 'artificial intelligence', 'machine learning', 'AI agent',
            'LLM', 'GPT', 'language model', 'deep learning',
            'AI generated', 'AI music', 'AI writing', 'AI code'
        ],
        '编程教育': [
            '编程教育', '编程学习', '少儿编程', '学编程',
            'programming', 'code', 'coding', 'developer',
            'JavaScript', 'Python', '编程思维', 'computational',
            'software', 'engineering', '程序员', '开发者'
        ],
        '写作表达': [
            '写作能力', '表达能力', '写作', '沟通',
            'writing', 'communication', 'language', 'Markdown',
            '技术写作', '表达', '演讲', 'debate',
            'natural language', 'interface', 'prompt'
        ],
        '网络安全': [
            '网络安全', '信息安全', '数据安全', '隐私保护',
            'security', 'privacy', 'password', 'encryption',
            'hacking', 'vulnerability', 'data breach', '安全'
        ],
        '学习方式': [
            '个性化学习', '自适应学习', '在线学习', '混合学习',
            '翻转课堂', '项目制学习', 'PBL', '探究式学习',
            '学习效率', '学习工具', '学习平台', '教育APP',
            '自主学习', '终身学习', '技能培养',
            'learning', 'education', 'tutorial', 'course'
        ],
        '教育趋势': [
            '教育', '学校', '老师', '学生',
            'education', 'school', 'teacher', 'student',
            'university', 'college', 'learning', 'teaching'
        ]
    }

    # 爆款标题模板 - 专门针对海外教育+AI
    TITLE_TEMPLATES = {
        '震撼型': [
            "😱 美国学校炸锅了！ChatGPT强制下架，校长这样说...",
            "💔 90%的家长还不知道！AI已经悄悄改变了美国教育",
            "⚠️ 紧急！常春藤名校最新政策：ChatGPT将被...",
            "❌ 别再糊涂了！关于AI教育，美国老师的真心话",
            "🚨 震撼教育部！这所学校全面禁用AI，结果..."
        ],
        '对比型': [
            "🤔 为什么美国孩子都在用AI学数学，我们还在...",
            "😱 同样的AI工具，中美教育差距竟然这么大！",
            "💡 看看芬兰怎么做的！AI时代的教育改革",
            "❌ 传统教育 VS AI教育，20年后差距令人窒息",
            "🔄 这波AI革命，为什么美国学校走在了前面？"
        ],
        '数据型': [
            "📊 数据说话：使用AI的孩子，成绩提升了200%！",
            "🔍 最新研究：美国85%的学校已引入AI教学",
            "💡 哈佛报告：AI时代，这5种能力比成绩更重要",
            "📈 投资1万元VS免费AI，教育回报率对比",
            "🎯 调查1000位美国妈妈：她们这样应对AI教育"
        ],
        '方法型': [
            "✨ 宝藏！美国名校都在用的AI学习法",
            "📚 建议收藏！我和孩子这样用ChatGPT学英语",
            "💪 亲测有效！美国妈妈的AI教育心得",
            "🎯 不花一分钱，复刻美国AI课堂的3个方法",
            "🌟 斯坦福教授推荐：AI时代这样培养孩子"
        ],
        '焦虑共鸣型': [
            "😭 看完美国教育现状，我失眠了",
            "💪 这才叫教育！看完差距我哭了",
            "❤️ 转发给焦虑的家长：AI时代我们要这样准备",
            "🙏 别让孩子输在AI时代，这篇一定要看",
            "😌 终于找到答案了，关于孩子未来的思考"
        ],
        '前瞻型': [
            "🔮 2030年的教育会怎样？美国校长告诉你",
            "💫 AI来了，孩子需要掌握的3种核心能力",
            "🚀 未来10年，这些孩子最有竞争力",
            "⚡ 教育革命已来，你还在用老方法吗？",
            "🌟 提前布局！AI时代的赢家教育法"
        ]
    }

    # 热门emoji
    EMOJIS = ['🔥', '⚠️', '✨', '💡', '❤️', '😱', '💔', '😭', '🙏', '📊',
              '🚨', '⚡', '🌟', '💎', '🎓', '🇺🇸', '🌍', '🤖', '💻', '🎯']

    # 小红书热门标签
    HASHTAGS = [
        '#AI教育', '#ChatGPT教育', '#海外教育', '#美国教育',
        '#教育科技', '#未来教育', '#学习方法', '#育儿心得',
        '#教育焦虑', '#AI时代', '#教育变革', '#国际教育',
        '#留学教育', '#素质教育', '#亲子教育', '#干货分享',
        '#美国学校', '#教育创新', '#学习工具', '#父母必看'
    ]

    def __init__(self):
        self.topics = []

    def load_topics_from_file(self, filepath):
        """从报告文件加载话题"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析话题
            self.topics = self._parse_topics(content)
            print(f"✓ 成功加载 {len(self.topics)} 条话题")
            return True
        except Exception as e:
            print(f"✗ 加载话题失败: {e}")
            return False

    def _parse_topics(self, content):
        """从Markdown内容解析话题"""
        topics = []
        lines = content.split('\n')

        current_platform = None
        for line in lines:
            # 检测平台
            if line.startswith('## 📱'):
                current_platform = line.replace('## 📱', '').strip()
            # 检测话题
            elif line.startswith('### '):
                title = line.replace('###', '').strip()
                # 提取排名和标题
                parts = title.split('. ', 1)
                if len(parts) == 2:
                    rank = parts[0]
                    title = parts[1].split('[')[0].strip()
                else:
                    title = title.strip()

                topics.append({
                    'platform': current_platform or 'Unknown',
                    'title': title,
                    'original': title
                })

        return topics

    def filter_parenting_topics(self):
        """筛选教育+AI话题"""
        filtered = []

        for topic in self.topics:
            title_lower = topic['title'].lower()

            # 检查是否包含相关关键词
            for category, keywords in self.PARENT_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in title_lower:
                        filtered.append({
                            **topic,
                            'category': category,
                            'keyword': keyword
                        })
                        break

        print(f"✓ 筛选出 {len(filtered)} 条教育+AI话题")
        return filtered

    def generate_titles(self, topic, count=10):
        """为话题生成爆款标题"""
        titles = []
        title = topic['title']

        # 提取关键信息
        key_info = self._extract_key_info(title)

        # 从不同模板生成标题
        for template_type, templates in self.TITLE_TEMPLATES.items():
            for template in templates[:2]:
                new_title = template

                # 替换占位符
                if '{}' in new_title:
                    new_title = new_title.format(key_info)
                else:
                    if not new_title.endswith('...'):
                        new_title = new_title + ' - ' + key_info[:20]

                # 添加emoji
                if not any(emoji in new_title for emoji in self.EMOJIS):
                    import random
                    emoji = random.choice(['🔥', '⚠️', '✨'])
                    new_title = emoji + ' ' + new_title

                titles.append({
                    'type': template_type,
                    'title': new_title.strip()
                })

                if len(titles) >= count:
                    return titles

        return titles[:count]

    def _extract_key_info(self, title):
        """提取标题关键信息"""
        for emoji in self.EMOJIS:
            title = title.replace(emoji, '')

        words = title.split()
        if len(words) > 8:
            key_info = ' '.join(words[:8]) + '...'
        else:
            key_info = title

        return key_info[:35]

    def _is_english(self, text):
        """检测文本是否主要为英文"""
        # 移除emoji和特殊字符
        text = re.sub(r'[^\w\s]', '', text)
        if not text:
            return False
        # 计算英文字符比例
        english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
        total_chars = sum(1 for c in text if c.isalpha())
        if total_chars == 0:
            return False
        return english_chars / total_chars > 0.6

    def _translate_title(self, title):
        """翻译英文标题为中文（保留原标题，添加中文说明）"""
        if not self._is_english(title):
            return title

        # 常见技术术语翻译字典
        translations = {
            # AI相关
            'AI': 'AI',
            'LLM': '大语言模型',
            'LLMs': '大语言模型',
            'GPT': 'GPT',
            'ChatGPT': 'ChatGPT',
            'OpenAI': 'OpenAI',
            'DeepSeek': 'DeepSeek',
            'Claude': 'Claude',
            'Gemini': 'Gemini',
            'machine learning': '机器学习',
            'deep learning': '深度学习',
            'neural network': '神经网络',
            'language model': '语言模型',
            'artificial intelligence': '人工智能',

            # 编程相关
            'programming': '编程',
            'code': '代码',
            'coding': '编程',
            'software': '软件',
            'developer': '开发者',
            'engineering': '工程',
            'JavaScript': 'JavaScript',
            'Python': 'Python',
            'Rust': 'Rust',
            'Java': 'Java',
            'API': 'API',
            'framework': '框架',
            'library': '库',

            # 教育相关
            'education': '教育',
            'learning': '学习',
            'tutorial': '教程',
            'course': '课程',
            'teacher': '老师',
            'student': '学生',
            'school': '学校',
            'university': '大学',
            'college': '学院',

            # 网络相关
            'security': '安全',
            'privacy': '隐私',
            'hacking': '黑客',
            'vulnerability': '漏洞',
            'password': '密码',
            'encryption': '加密',
            'data breach': '数据泄露',

            # 工具相关
            'tool': '工具',
            'platform': '平台',
            'system': '系统',
            'application': '应用',
            'app': '应用',
            'service': '服务',
            'feature': '功能',

            # 通用词汇
            'how to': '如何',
            'guide': '指南',
            'best': '最佳',
            'top': '顶级',
            'vs': '对决',
            'versus': '对决',
            'why': '为什么',
            'what': '什么',
            'how': '如何',
            'tips': '技巧',
            'tricks': '技巧',
            'secrets': '秘密',
            'introduction': '介绍',
            'overview': '概述',
            'analysis': '分析',
            'review': '评测',
            'comparison': '对比',
        }

        # 生成中文说明
        chinese_desc = ""

        # 尝试提取关键词并生成说明
        title_upper = title.upper()
        title_lower = title.lower()

        # AI相关
        if 'LLM' in title_upper or 'GPT' in title_upper or 'Claude' in title or 'Gemini' in title or 'OpenAI' in title:
            if any(word in title_lower for word in ['education', 'learning', 'teaching', 'school']):
                chinese_desc = "AI如何改变教育"
            elif any(word in title_lower for word in ['future', 'impact', 'revolution', 'transform']):
                chinese_desc = "AI对未来的影响"
            else:
                chinese_desc = "关于大语言模型的热议"
        elif 'AI' in title_upper or 'artificial intelligence' in title_lower:
            if any(word in title_lower for word in ['education', 'learning', 'teaching']):
                chinese_desc = "AI在教育中的应用"
            elif any(word in title_lower for word in ['ethics', 'safety', 'risk', 'danger']):
                chinese_desc = "AI的伦理与安全"
            else:
                chinese_desc = "关于人工智能的讨论"

        # 编程相关
        elif any(word in title_lower for word in ['programming', 'code', 'coding', 'developer', 'software']):
            if any(word in title_lower for word in ['education', 'learning', 'tutorial', 'beginner']):
                chinese_desc = "编程教育话题"
            elif any(word in title_lower for word in ['language', 'javascript', 'python', 'rust', 'java']):
                chinese_desc = "编程语言讨论"
            else:
                chinese_desc = "软件开发相关"

        # 安全相关
        elif any(word in title_lower for word in ['security', 'privacy', 'hacking', 'vulnerability', 'password']):
            chinese_desc = "网络安全话题"

        # 教育/学习相关
        elif any(word in title_lower for word in ['education', 'learning', 'school', 'university', 'college']):
            if any(word in title_lower for word in ['online', 'remote', 'digital']):
                chinese_desc = "在线教育话题"
            else:
                chinese_desc = "教育创新讨论"

        # 工具/平台相关
        elif any(word in title_lower for word in ['tool', 'platform', 'system', 'application', 'app']):
            chinese_desc = "实用工具推荐"

        # 通用技术讨论
        elif any(word in title_lower for word in ['technology', 'tech', 'digital', 'innovation']):
            chinese_desc = "科技前沿讨论"

        # 如果无法识别，使用通用说明
        else:
            chinese_desc = "海外科技热点"

        # 组合结果：保留英文原标题 + 添加中文说明
        if len(title) > 50:
            # 标题太长，截断
            title_short = title[:47] + "..."
            return f"{title_short}\n（{chinese_desc}）"
        else:
            return f"{title}\n（{chinese_desc}）"

    def generate_content(self, topic):
        """生成小红书内容"""
        category = topic.get('category', '')
        keyword = topic.get('keyword', '')
        title = topic['title']

        # 根据分类生成内容
        if 'AI变革' in category or 'AI' in keyword:
            return self._generate_ai_revolution_content(topic)
        elif '海外' in category or '美国' in keyword or '欧洲' in keyword:
            return self._generate_overseas_content(topic)
        elif '争议' in category:
            return self._generate_controversy_content(topic)
        elif '焦虑' in category:
            return self._generate_anxiety_content(topic)
        else:
            return self._generate_general_content(topic)

    def _generate_ai_revolution_content(self, topic):
        """生成AI变革内容"""
        title = topic['title']
        translated_title = self._translate_title(title)

        content = f"""
🤖 AI真的要颠覆教育了吗？

最近看到这个消息：
【{translated_title}】

说实话，看完我的第一反应是：
😱 我们的孩子准备好迎接AI时代了吗？

🇺🇸 美国学校已经在行动：
✅ 77%的学区开始试点AI教学
✅ ChatGPT被纳入部分课程
✅ 个性化AI tutor普及

💡 为什么他们这么做？

因为美国教育界认识到：
❌ 封堵AI不是办法
✅ 教会孩子正确使用才是关键

🎯 我们能学到什么？

1️⃣ 不要把AI当洪水猛兽
   它是工具，关键是怎么用

2️⃣ 培养AI思维
   - 批判性思维
   - 信息鉴别能力
   - 人机协作能力

3️⃣ 关注软技能
   - 创造力（AI不会）
   - 情商（更重要了）
   - 适应性（快速学习）

💪 未来的竞争
不是人和AI的竞争
而是会用AI的人 vs 不会用AI的人

❤️ 觉得有用请点赞收藏
转发给更多家长看到💕

{self._get_random_hashtags()}

👇 评论区：你会让孩子用AI学习吗？
        """.strip()

        return content

    def _generate_overseas_content(self, topic):
        """生成海外教育实践内容"""
        title = topic['title']
        translated_title = self._translate_title(title)

        content = f"""
🌍 看看海外是怎么应对AI教育的！

【{translated_title}】

最近一直在研究海外教育动态
发现了一些很有意思的实践👀

🇺🇸 美国的做法：
✅ 部分州允许学生用ChatGPT辅助学习
✅ 教会学生如何鉴别AI生成的信息
✅ 把AI检测和识别纳入课程
✅ 重视prompt engineering（提示词工程）

🇫🇷 芬兰的创新：
✅ AI辅助个性化学习路径
✅ 减少机械性作业，增加创造性任务
✅ 教师角色转变为引导者

🇸🇬 新加坡的平衡：
✅ 既不禁止也不鼓励，规范使用
✅ 制定AI使用伦理准则
✅ 重视传统基础能力+AI技能

💡 他们的共同点：
❌ 不是简单禁止或开放
✅ 而是系统性地应对

🎯 给我们的启发：

1️⃣ 教育要与时俱进
   AI来了，教育方式必须改变

2️⃣ 培养辨别能力
   学会判断信息真伪更重要

3️⃣ 重视能力培养
   而不是死记硬背

4️⃣ 教师需要转型
   从知识传授者到能力培养者

💪 我们不需要照搬
但可以借鉴他们的思路

❤️ 觉得有用请点赞收藏
转发给更多家长💕

{self._get_random_hashtags()}

👇 你支持哪种教育方式？
        """.strip()

        return content

    def _generate_controversy_content(self, topic):
        """生成争议冲突内容"""
        title = topic['title']
        translated_title = self._translate_title(title)

        content = f"""
⚠️ ChatGPT进入校园，教育界吵翻了！

【{translated_title}】

最近这个话题在国外教育圈炸锅了🔥

🚫 反对派说：
❌ 这是作弊！破坏学术诚信
❌ 学生会过度依赖AI
❌ 老师无法判断学生真实水平
❌ 加剧教育不公平

✅ 支持派说：
✅ 这是生产力工具，为什么要禁止？
✅ 就像当年计算器一样
✅ 关键是教会学生正确使用
✅ 可以帮助老师减轻负担

💔 我的思考：

其实两派都有道理
但关键问题可能是：
🎯 我们的教育目标是什么？

如果目标是：
❌ 死记硬背 → AI确实有威胁
✅ 培养能力 → AI是强大的助手

🌟 美国一些学校的做法：

1️⃣ 明确使用规范
   什么时候可以用，什么时候不行

2️⃣ 重新设计作业
   更注重思考和过程
   而不是标准答案

3️⃣ 教会AI素养
   如何正确使用工具
   如何鉴别信息真伪

💪 时代在变
我们的教育也必须改变

禁止不是办法
引导才是关键❤️

{self._get_random_hashtags()}

👇 你支持校园里使用ChatGPT吗？
        """.strip()

        return content

    def _generate_anxiety_content(self, topic):
        """生成教育焦虑内容"""
        title = topic['title']
        translated_title = self._translate_title(title)

        content = f"""
💔 看完这个，作为家长我彻夜难眠...

【{translated_title}】

最近AI教育的话题越来越火
朋友圈里全是：
"美国孩子都在用AI学数学了"
"不会用AI的孩子会被淘汰"
...

说实话，我也有点慌😰

🤔 我们在焦虑什么？

❌ 怕孩子输在起跑线
❌ 怕跟不上时代
❌ 怕未来的竞争
❌ 怕自己做得不够

但是...
冷静下来想想：
📊 85%的美国家长也在焦虑同样的问题

🌟 一些思考：

1️⃣ AI是工具，不是目标
   学会使用比拥有更重要

2️⃣ 核心能力不会过时
   - 批判性思维
   - 创造力
   - 情商和沟通
   这些AI替代不了

3️⃣ 适合孩子的才是最好的
   不是所有孩子都要学编程
   不是所有孩子都要用AI

💡 我现在这样做：

✅ 了解AI但不盲从
✅ 关注孩子的兴趣和特点
✅ 培养底层能力而不是技能
✅ 给孩子选择的权利

💪 育儿路上
我们都是第一次
不必焦虑，一起成长❤️

{self._get_random_hashtags()}

👇 你对AI教育焦虑吗？评论区聊聊
        """.strip()

        return content

    def _generate_general_content(self, topic):
        """生成通用内容"""
        title = topic['title']
        translated_title = self._translate_title(title)

        content = f"""
✨ 今天看到一个教育话题，很有感触

【{translated_title}】

作为父母
我们总是在学习
在成长的路上
和孩子一起进步👨‍👩‍👧‍👦

💡 我的思考：

AI时代的教育
确实充满挑战
但也充满机会

📝 给大家的小建议：

1️⃣ 保持开放心态
   新技术不可怕
   可怕的是拒绝改变

2️⃣ 关注底层能力
   - 学习能力
   - 思考能力
   - 创造能力
   这些比知识更重要

3️⃣ 适合最重要
   每个孩子不同
   找到适合的方式

4️⃣ 陪伴是最珍贵的
   再好的AI工具
   也替代不了父母的陪伴

💪 未来属于
会拥抱变化的人

❤️ 育儿路上
一起学习，一起成长

{self._get_random_hashtags()}
        """.strip()

        return content

    def _get_random_hashtags(self):
        """获取随机标签"""
        import random
        return ' '.join(random.sample(self.HASHTAGS, 8))

    def generate_xiaohongshu_post(self, topic, title_count=5):
        """生成完整的小红书帖子"""
        print(f"\n{'='*70}")
        print(f"📝 原话题: {topic['title']}")
        print(f"📱 来源: {topic['platform']}")
        print(f"🏷️ 分类: {topic.get('category', '未知')}")
        print(f"{'='*70}\n")

        # 生成标题
        print("🎯 推荐标题（点击率优化版）：\n")
        titles = self.generate_titles(topic, title_count)

        for i, t in enumerate(titles, 1):
            print(f"{i}. 【{t['type']}】")
            print(f"   {t['title']}")
            print()

        # 生成正文
        print("\n" + "="*70)
        print("📄 正文内容（已优化互动）：\n")
        content = self.generate_content(topic)
        print(content)

        # 生成图片/视频建议
        image_suggestions = self._generate_image_suggestions(topic)

        # 添加建议
        print("\n" + "="*70)
        print("💡 发布建议：\n")
        print("✅ 最佳发布时间：")
        print("   工作日：7:00-9:00, 21:00-23:00")
        print("   周末：9:00-11:00, 20:00-22:00")
        print()
        print("✅ 封面图建议：")
        for suggestion in image_suggestions[:3]:
            print(f"   - {suggestion}")
        print()
        print("✅ 互动技巧：")
        print("   - 提问：'你家孩子用过AI学习吗？'")
        print("   - 投票：'支持校园使用ChatGPT吗？'")
        print("   - 征集：'分享你的AI教育经验'")
        print()

        return {
            'titles': titles,
            'content': content,
            'topic': topic,
            'image_suggestions': image_suggestions,
            'video_suggestions': self._generate_video_suggestions(topic)
        }

    def _generate_image_suggestions(self, topic):
        """生成配图建议"""
        suggestions = [
            "孩子使用平板/电脑学习的照片（真实场景）",
            "教育相关的图片（学校、书本、黑板等）",
            "添加醒目文字：'AI改变教育'、'美国学校'等",
            "对比图：传统学习 VS AI辅助学习",
            "数据图表：使用Canva制作教育相关数据可视化",
            "emoji图标：🤖💡📚✨等增强视觉效果",
            "红底白字或黄黑搭配的醒目标题图"
        ]

        # 根据分类添加特定建议
        category = topic.get('category', '')
        if 'AI' in category:
            suggestions.append("AI机器人、ChatGPT界面截图")
            suggestions.append("未来科技感的背景图")
        elif '海外' in category or '美国' in category:
            suggestions.append("美国校园、教室照片")
            suggestions.append("国旗emoji：🇺🇸🇫🇮🇸🇬")

        return suggestions

    def _generate_video_suggestions(self, topic):
        """生成视频建议"""
        return [
            "录制孩子使用AI工具学习的真实场景（15-30秒）",
            "对比视频：传统学习 VS AI辅助学习的效果",
            "访谈视频：孩子/家长对AI教育的看法",
            "屏幕录制：演示如何使用AI学习工具",
            "动画视频：解释AI在教育中的应用",
            "数据动画：展示教育AI的发展趋势"
        ]


def main():
    """主函数"""
    print("="*70)
    print("🔥 小红书爆文生成器 - 海外教育AI专题")
    print("="*70)
    print()

    # 初始化生成器
    generator = XiaohongshuGenerator()

    # 初始化话题追踪器
    tracker = TopicTracker()
    tracker.print_stats()

    # 查找最新的报告文件
    import glob
    output_files = glob.glob('output/hot_topics_*.md')

    if not output_files:
        print("❌ 未找到报告文件")
        print("请先运行以下命令生成数据：")
        print()
        print("docker run --rm -e USE_PROXY=true -e PROXY_HOST=host.docker.internal \\")
        print("  -e PROXY_PORT=10810 -e YOUTUBE_API_KEY='你的密钥' \\")
        print("  -v 'D:\\Projects\\ClaudeCode\\topicgenerater:/app' -w /app \\")
        print("  python:3.8-slim python main.py")
        return

    # 按时间排序，取最新的
    latest_file = max(output_files)
    print(f"📂 读取文件: {latest_file}\n")

    # 加载话题
    if not generator.load_topics_from_file(latest_file):
        return

    # 筛选教育+AI话题
    print("\n[*] 正在筛选海外教育+AI话题...")
    parenting_topics = generator.filter_parenting_topics()

    if not parenting_topics:
        print("❌ 未找到相关话题")
        print()
        print("💡 建议：")
        print("1. 确保Hacker News和YouTube数据获取成功")
        print("2. 这些平台包含更多海外教育AI话题")
        return

    # 过滤已使用的话题（30天内）
    print("\n[*] 正在过滤已使用的话题（30天内）...")
    unused_topics = tracker.filter_unused_topics(parenting_topics, days=30)

    if not unused_topics:
        print("⚠️ 所有筛选的话题都在最近30天内已使用")
        print()
        print("💡 建议：")
        print("1. 调整days参数查看更早的话题")
        print("2. 或者等待新的热点话题出现")

        # 显示已使用的话题
        print("\n已使用的话题:")
        for topic in parenting_topics[:5]:
            title = topic.get('title', '未知')
            print(f"  - {title}")

        return

    print(f"✓ 原始话题数: {len(parenting_topics)}")
    print(f"✓ 未使用话题数: {len(unused_topics)}")
    print(f"✓ 过滤掉: {len(parenting_topics) - len(unused_topics)} 个已使用话题")

    # 选择最热门的5个话题（或全部，如果不足5个）
    print("\n[*] 选择最适合的话题...")
    selected_topics = unused_topics[:5]

    print(f"\n✓ 为您生成 {len(selected_topics)} 个小红书爆文内容\n")

    # 为每个话题生成完整帖子
    results = []
    for i, topic in enumerate(selected_topics, 1):
        print(f"\n{'#'*70}")
        print(f"# 爆文 {i}/{len(selected_topics)}")
        print(f"{'#'*70}")

        result = generator.generate_xiaohongshu_post(topic)
        results.append(result)

        # 标记话题为已使用
        tracker.mark_topic_used(
            topic['title'],
            metadata={
                'platform': topic.get('platform', ''),
                'category': topic.get('category', ''),
                'url': topic.get('url', ''),
                'generated_at': datetime.now().isoformat()
            }
        )
        print(f"✓ 已标记话题为已使用")

    # 保存到CSV文件
    from src.exporter_csv import CSVExporter
    csv_exporter = CSVExporter()

    # 准备CSV数据
    csv_data = []
    for result in results:
        # 为每个标题创建一行数据
        for title_info in result['titles']:
            csv_data.append({
                'original_topic': result['topic']['title'],
                'platform': result['topic']['platform'],
                'category': result['topic'].get('category', '未知'),
                'title_type': title_info['type'],
                'title': title_info['title'],
                'content': result['content'],
                'image_suggestions': ' | '.join(result['image_suggestions'][:3]),
                'video_suggestions': ' | '.join(result['video_suggestions'][:2]),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    # 导出CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = csv_exporter.export_xiaohongshu_posts(csv_data, f'xiaohongshu_posts_{timestamp}.csv')

    # 同时保存Markdown文件（可选）
    md_file = f"output/xiaohongshu_AI教育_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 🔥 小红书爆文合集 - 海外教育AI专题\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"总篇数: {len(results)}\n")
        f.write(f"主题: 海外传统教育如何应对AI变革\n\n")
        f.write("="*70 + "\n\n")

        for i, result in enumerate(results, 1):
            f.write(f"## 爆文 {i}: {result['topic']['title']}\n\n")
            f.write(f"**来源**: {result['topic']['platform']}\n")
            f.write(f"**分类**: {result['topic'].get('category', '未知')}\n\n")

            f.write("### 🎯 推荐标题\n\n")
            for j, title in enumerate(result['titles'], 1):
                f.write(f"{j}. {title['title']}\n")

            f.write("\n### 📄 正文内容\n\n")
            f.write(result['content'])
            f.write("\n\n" + "="*70 + "\n\n")

    print(f"\n✅ CSV已保存到: {csv_file}")
    print(f"✅ Markdown已保存到: {md_file}")
    print("\n🎉 生成完成！")

    # 显示更新后的统计信息
    print("\n")
    tracker.print_stats()
    print()
    print("💡 使用建议：")
    print("1. 选择最适合的标题")
    print("2. 根据实际情况微调内容")
    print("3. 添加真实图片（孩子学习场景、教育相关）")
    print("4. 发布后积极回复评论区")
    print()
    print("📊 CSV文件可用Excel打开，方便编辑和管理")


if __name__ == '__main__':
    main()
