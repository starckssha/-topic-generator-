"""
爆文生成服务
将现有的爆文生成逻辑改造为服务类，集成到数据库
"""
import os
import sys
import re
import random
import threading
from datetime import datetime
from typing import List, Dict, Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.models import ViralPost, TaskExecution, UsedTopic
from src.database.repositories import ViralPostRepository, TaskExecutionRepository, UsedTopicRepository, HotTopicRepository
from src.services.ai_service import AIService


class GenerateProgress:
    """生成进度数据类"""

    def __init__(self):
        self.total_topics = 0
        self.completed_topics = 0
        self.current_topic = ""
        self.results = []
        self.status = "pending"  # pending, running, success, failed
        self.error_message = None

    def to_dict(self):
        return {
            'total_topics': self.total_topics,
            'completed_topics': self.completed_topics,
            'progress': (self.completed_topics / self.total_topics * 100) if self.total_topics > 0 else 0,
            'current_topic': self.current_topic,
            'results': self.results,
            'status': self.status,
            'error_message': self.error_message
        }


class GenerateService:
    """爆文生成服务类"""

    # AI+管理/职业/转型/失业应对关键词库
    PARENT_KEYWORDS = {
        'AI变革': [
            'AI', 'artificial intelligence', 'machine learning', 'AI agent',
            'LLM', 'GPT', 'ChatGPT', 'OpenAI', 'Claude', 'Gemini',
            'language model', 'deep learning', 'neural network',
            'AI generated', 'AI music', 'AI writing', 'AI code',
            'automation', 'robot', '机器人', '自动化',
            'AI革命', '技术变革', 'tech revolution', 'disruption'
        ],
        '管理': [
            '管理', 'management', 'manager', 'leader', 'leadership',
            'CEO', 'CTO', '高管', '中层管理', '团队管理',
            'project management', 'productivity', '效率',
            'decision making', '决策', '战略', 'strategy',
            '企业管理', '公司管理', '组织管理', '绩效管理',
            'HR', '人力资源', '招骋', 'hiring', 'recruitment',
            'AI管理', 'AI辅助管理', '智能管理'
        ],
        '职业规划': [
            'career', '职业', 'job', 'work', 'employment',
            '职业规划', 'career path', '职业发展', 'career development',
            '晋升', 'promotion', '薪资', 'salary', 'pay',
            '求职', 'job hunting', '找工作', '面试', 'interview',
            '技能', 'skills', '能力', 'ability', 'competency',
            '职业转型', 'career transition', '转行', 'career change',
            'AI职业', 'future of work', '工作未来', '职业技能'
        ],
        '转型': [
            '转型', 'transition', 'transform', 'change',
            '职业转型', 'career transition', '行业转型', 'industry shift',
            '技能转型', 'reskilling', 'upskilling', '再培训',
            '学习新技能', 'new skills', 'adapt', '适应',
            'digital transformation', '数字化转型',
            'AI转型', '技术转型', 'business transformation',
            '转型成功', '转型失败', '转型案例', '转型经验'
        ],
        '失业应对': [
            '失业', 'unemployment', 'unemployed', 'layoff', 'fired',
            '裁员', 'job cut', 'redundancy', '下岗',
            '失业率', 'unemployment rate', 'jobless rate',
            'AI替代', 'AI replacement', 'automation job', '自动化替代',
            '失业应对', 'cope with unemployment', '应对裁员',
            '再就业', 're-employment', '重新开始', 'fresh start',
            '失业保险', 'unemployment benefits', '失业救济',
            '职场生存', 'workplace survival', 'job security', '工作保障'
        ]
    }

    # 爆款标题模板
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
        self.progress_store = {}
        self.lock = threading.Lock()
        self.ai_service = AIService()

    def is_education_ai_topic(self, topic_title: str) -> tuple:
        """
        判断话题是否与教育+AI相关

        Returns:
            (is_relevant: bool, matched_category: str)
        """
        title_lower = topic_title.lower()

        for category, keywords in self.PARENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return True, category

        return False, None

    def generate_viral_posts(
        self,
        topic_ids: List[int],
        use_ai: bool = False,
        title_types: List[str] = None,
        async_execution: bool = False
    ) -> Dict:
        """
        生成爆文

        Args:
            topic_ids: 热点话题ID列表
            use_ai: 是否使用AI增强
            title_types: 标题类型列表，None则使用全部
            async_execution: 是否异步执行

        Returns:
            执行结果
        """
        # 生成批次ID
        batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 初始化进度
        progress = GenerateProgress()
        self.progress_store[batch_id] = progress

        if async_execution:
            # 异步执行
            thread = threading.Thread(
                target=self._generate_worker,
                args=(batch_id, topic_ids, use_ai, title_types, progress)
            )
            thread.start()
            return {
                'batch_id': batch_id,
                'status': 'running',
                'message': '生成任务已启动（异步执行）'
            }
        else:
            # 同步执行
            return self._generate_worker(batch_id, topic_ids, use_ai, title_types, progress)

    def _generate_worker(
        self,
        batch_id: str,
        topic_ids: List[int],
        use_ai: bool,
        title_types: List[str],
        progress: GenerateProgress
    ) -> Dict:
        """
        生成工作线程

        Args:
            batch_id: 批次ID
            topic_ids: 话题ID列表
            use_ai: 是否使用AI
            title_types: 标题类型
            progress: 进度对象

        Returns:
            执行结果
        """
        start_time = datetime.now()

        # 创建任务记录
        task = TaskExecution(
            task_type='generate_viral_posts',
            batch_id=batch_id,
            status='running',
            start_time=start_time,
            triggered_by='manual'
        )
        task_id = TaskExecutionRepository.insert(task)

        progress.total_topics = len(topic_ids)
        progress.status = "running"

        # 获取话题数据
        topics = []
        for topic_id in topic_ids:
            topic = HotTopicRepository.get_by_id(topic_id)
            if topic:
                topics.append(topic)

        # 筛选教育+AI相关话题
        education_ai_topics = []
        filtered_topics = []

        for topic in topics:
            is_relevant, category = self.is_education_ai_topic(topic.title)
            if is_relevant:
                topic.category = category  # 更新分类
                education_ai_topics.append(topic)
            else:
                # 暂时不过滤，标记为通用类
                topic.category = '通用'
                education_ai_topics.append(topic)

        print(f"🚀 开始生成爆文（批次: {batch_id}）")
        print(f"原始话题数: {len(topics)}")
        print(f"教育+AI相关: {len([t for t in topics if self.is_education_ai_topic(t.title)[0]])}")
        print(f"通用话题: {len([t for t in topics if not self.is_education_ai_topic(t.title)[0]])}")

        # 只处理教育+AI相关话题
        topics = education_ai_topics

        if not topics:
            print("⚠️ 没有找到可用的话题")
            return {
                'batch_id': batch_id,
                'status': 'success',
                'total': len(topic_ids),
                'success': 0,
                'failed': 0,
                'total_posts': 0,
                'filtered': len(filtered_topics),
                'message': '没有找到可用的话题'
            }

        all_posts = []
        used_topics_list = []

        for topic in topics:
            progress.current_topic = topic.title
            try:
                # 生成多个标题变体
                posts = self._generate_posts_for_topic(
                    topic,
                    batch_id,
                    title_types
                )

                all_posts.extend(posts)

                # 标记话题为已使用
                used_topic = UsedTopic(
                    normalized_title=UsedTopic.normalize_title(topic.title),
                    original_title=topic.title,
                    platform=topic.platform,
                    category=topic.category,
                    url=topic.url,
                    used_at=start_time,
                    metadata={
                        'hot_topic_id': topic.id,
                        'batch_id': batch_id
                    }
                )
                used_topics_list.append(used_topic)

                progress.completed_topics += 1
                progress.results.append({
                    'topic_id': topic.id,
                    'title': topic.title,
                    'status': 'success',
                    'post_count': len(posts)
                })

            except Exception as e:
                print(f"[!] 生成失败 ({topic.title}): {e}")
                progress.results.append({
                    'topic_id': topic.id,
                    'title': topic.title,
                    'status': 'failed',
                    'error': str(e)
                })
                progress.completed_topics += 1

        # 批量保存到数据库
        if all_posts:
            ViralPostRepository.batch_insert(all_posts)
            print(f"✓ 保存了 {len(all_posts)} 篇爆文到数据库")

        if used_topics_list:
            UsedTopicRepository.batch_insert(used_topics_list)
            print(f"✓ 标记了 {len(used_topics_list)} 个话题为已使用")

        # 标记话题为已生成（避免重复生成）
        generated_at = datetime.now()
        marked_count = 0
        for topic_id in topic_ids:
            if HotTopicRepository.mark_as_generated(topic_id, generated_at):
                marked_count += 1
        print(f"✓ 标记了 {marked_count} 个话题为已生成（避免重复）")

        # 更新任务记录
        end_time = datetime.now()
        duration_seconds = int((end_time - start_time).total_seconds())

        task_result = {
            'total': len(topic_ids),
            'success': len([r for r in progress.results if r['status'] == 'success']),
            'failed': len([r for r in progress.results if r['status'] == 'failed']),
            'total_posts': len(all_posts)
        }
        task.set_result_summary(task_result)

        TaskExecutionRepository.update_status(
            task_id,
            'success',
            end_time=end_time,
            duration_seconds=duration_seconds
        )

        progress.status = "success"

        return {
            'batch_id': batch_id,
            'status': 'success',
            'total': len(topic_ids),
            'success': task_result['success'],
            'failed': task_result['failed'],
            'total_posts': len(all_posts),
            'duration_seconds': duration_seconds
        }

    def _generate_posts_for_topic(
        self,
        topic,
        batch_id: str,
        title_types: List[str] = None
    ) -> List[ViralPost]:
        """为单个话题生成多个爆文"""
        posts = []

        # 确定标题类型
        if title_types is None:
            title_types = list(self.TITLE_TEMPLATES.keys())

        # 为每种标题类型生成一个爆文
        for title_type in title_types:
            title = self._generate_title(topic.title, title_type)
            content = self._generate_content(topic, title_type)

            post = ViralPost(
                hot_topic_id=topic.id,
                original_topic=topic.title,
                source_platform=topic.platform,
                topic_category=topic.category,
                title_type=title_type,
                recommended_title=title,
                content=content,
                image_suggestions=self._generate_image_suggestions(topic),
                video_suggestions=self._generate_video_suggestions(topic),
                generated_at=datetime.now(),
                batch_id=batch_id,
                is_published=0
            )
            posts.append(post)

        return posts

    def _generate_title(self, topic_title: str, title_type: str) -> str:
        """生成标题"""
        templates = self.TITLE_TEMPLATES.get(title_type, self.TITLE_TEMPLATES['震撼型'])
        template = random.choice(templates)

        # 如果模板有占位符，填充关键信息
        if '{}' in template:
            key_info = self._extract_key_info(topic_title)
            return template.format(key_info)

        # 否则添加话题信息
        if not template.endswith('...'):
            return f"{template} - {topic_title[:30]}"

        return template

    def _extract_key_info(self, title: str) -> str:
        """提取标题关键信息"""
        for emoji in self.EMOJIS:
            title = title.replace(emoji, '')

        words = title.split()
        if len(words) > 8:
            key_info = ' '.join(words[:8]) + '...'
        else:
            key_info = title

        return key_info[:35]

    def _generate_content(self, topic, title_type: str) -> str:
        """
        生成正文内容（智能扩写）
        根据话题和标题类型，使用AI生成不同的内容
        """
        # 构建prompt，根据标题类型生成不同风格的内容
        style_prompts = {
            '震撼型': "写一篇小红书震撼型内容，开头要用震惊的语气，强调这个话题对职场和管理的重要性",
            '对比型': "写一篇对比型小红书内容，对比AI时代与传统时代的管理/职业差异",
            '数据型': "写一篇数据支撑型小红书内容，用具体数据说明AI对管理、职业、转型的影响",
            '方法型': "写一篇实用方法型小红书内容，分享具体的AI辅助管理、职业规划、转型步骤和经验",
            '焦虑共鸣型': "写一篇引发共鸣的小红书内容，从职场焦虑、失业恐惧切入，给出解决方案",
            '前瞻型': "写一篇前瞻型小红书内容，预测AI时代的管理和职业趋势，给出建议"
        }

        style_prompt = style_prompts.get(title_type, style_prompts['震撼型'])

        # 使用AI生成内容
        try:
            ai_content = self.ai_service.generate_content_for_topic(
                topic_title=topic.title,
                platform=topic.platform,
                category=topic.category,
                style=style_prompt,
                title_type=title_type
            )
            return ai_content
        except Exception as e:
            print(f"⚠️ AI生成失败，使用备用模板: {e}")
            # 如果AI失败，使用备用模板
            return self._generate_fallback_content(topic, title_type)

    def _generate_fallback_content(self, topic, title_type: str) -> str:
        """备用内容生成（当AI失败时使用）"""
        hashtags = ' '.join(random.sample(self.HASHTAGS, 5))

        base_template = f"""基于"{topic.title}"的深度分析

{topic.platform}平台热议话题

这个话题反映了当前教育+AI领域的重要趋势：

💡 核心观点：
1. AI正在改变教育方式
2. 我们需要适应新变化
3. 关键在于如何正确使用

🎯 建议：
✅ 拥抱AI工具
✅ 保持批判性思维
✅ 培养创造力

{hashtags}

#AI教育 #教育变革"""

        return base_template

    def _content_shocking(self) -> str:
        """震撼型内容模板"""
        return """🤖 AI真的要颠覆教育了吗？

看到"{topic}"这个消息，我彻底震惊了！

美国的教育圈已经炸锅了！ChatGPT的疯狂进化，让所有教育者都在重新思考：

💡 我们的教育跟不上了吗？

📌 3个关键洞察：
1️⃣ AI不是敌人，是工具
2️⃣ 学会提问比学会回答更重要
3️⃣ 创造力将成为核心竞争力

🎯 给家长的建议：
✅ 不要完全禁止AI使用
✅ 引导孩子正确使用AI工具
✅ 培养孩子AI无法替代的能力

💪 AI时代，我们和孩子一起成长！

{hashtags}

#AI教育 #教育变革 #未来教育"""

    def _content_comparison(self) -> str:
        """对比型内容模板"""
        return """🤔 为什么美国孩子都在用AI，我们还在犹豫？

最近"{topic}"这个话题引起热议...

对比中美教育现状，差距令人深思：

📊 美国学校：
✅ 85%已引入AI教学
✅ 老师主动学习AI工具
✅ 学生用AI辅助学习
✅ 重视AI素养培养

📚 我们的现状：
⚠️ 大多数还在观望
⚠️ 担心AI影响学习
⚠️ 缺乏系统性指导
⚠️ AI教育刚刚起步

💡 关键不在于用什么工具，而在于怎么用！

🎯 给家长的建议：
1️⃣ 了解AI在教育中的正确用法
2️⃣ 引导孩子批判性思考
3️⃣ 平衡传统学习和AI辅助

{hashtags}

#教育差距 #AI教育 #学习方法"""

    def _content_data(self) -> str:
        """数据型内容模板"""
        return """📊 数据说话：AI教育的真实效果

"{topic}" - 这个数据太震撼了！

🔍 最新研究显示：
✨ 使用AI的学生，成绩平均提升30%
✨ 学习效率提高50%
✨ 85%的学生表示更有学习兴趣

📈 美国教育数据：
• 2024年：85%的学校引入AI
• 2023年：仅45%
• 增长率：+89% 🚀

💡 为什么效果这么好？
1️⃣ 个性化学习路径
2️⃣ 即时反馈机制
3️⃣ 激发学习兴趣
4️⃣ 释放创造潜能

⚠️ 但前提是：
✅ 正确使用AI工具
✅ 保持批判性思维
✅ 不能完全依赖AI

{hashtags}

#AI教育 #教育数据 #学习效果"""

    def _content_method(self) -> str:
        """方法型内容模板"""
        return """✨ 宝藏方法！美国名校都在用

"{topic}" - 分享一个超实用的AI学习法

📚 我和孩子的实践心得：

第一步：明确学习目标
🎯 不要直接问答案
🎯 让AI帮助你理解概念
🎯 引导思考而不是替代思考

第二步：学会提问技巧
✅ "请解释这个概念"
✅ "给我举例说明"
✅ "这样理解对吗"
✅ "为什么是这样"

第三步：验证和扩展
📖 查阅其他资料验证
📖 让AI举更多例子
📖 尝试用自己的话复述

💪 使用一个月后：
📈 学习兴趣明显提高
📈 理解能力显著增强
📈 主动思考更多了

{hashtags}

#学习方法 #AI学习 #教育心得"""

    def _content_anxiety(self) -> str:
        """焦虑共鸣型内容模板"""
        return """😭 看完这个，我失眠了一整夜

"{topic}"

作为一个家长，我真的焦虑了...

💔 我们的担忧：
❌ 孩子会被AI取代吗？
❌ 现在的学习还有意义吗？
❌ 怎样才能不输在AI时代？

💪 但焦虑解决不了问题！

🎯 我们应该这样做：
1️⃣ 拥抱变化，而不是抗拒
2️⃣ 培养AI无法替代的能力
   - 创造力
   - 批判性思维
   - 情商和沟通
   - 复杂问题解决
3️⃣ 让孩子成为AI的主人

🌟 AI时代，我们的孩子更需要：
✅ 终身学习的能力
✅ 适应变化的能力
✅ 人际协作的能力

❤️ 转发给同样焦虑的家长

{hashtags}

#教育焦虑 #AI时代 #育儿心得"""

    def _content_forward(self) -> str:
        """前瞻型内容模板"""
        return """🔮 2030年的教育会怎样？

"{topic}" - 这个信号太明显了！

📈 AI正在重塑教育的未来：

🚀 5大趋势预测：
1️⃣ AI个性化教学成为标配
2️⃣ 传统考试方式被颠覆
3️⃣ 学习不再受时空限制
4️⃣ 教师角色发生转变
5️⃣ 终身学习成为常态

💡 未来最需要的能力：
🎯 创造力和想象力
🎯 批判性思维
🎯 情感智能
🎯 跨学科整合
🎯 人机协作

🌟 给家长的建议：
✅ 不要只盯着分数
✅ 重视素质教育
✅ 培养学习兴趣
✅ 提前规划未来

{hashtags}

#未来教育 #AI教育 #教育趋势"""

    def _generate_image_suggestions(self, topic) -> str:
        """生成配图建议"""
        suggestions = [
            "1. 信息图：AI在教育中的应用数据对比",
            "2. 截图：AI工具界面展示",
            "3. 对比图：传统学习 VS AI辅助学习",
            "4. 思维导图：AI时代必备能力",
            "5. 示意图：AI学习流程",
            "6. 统计图表：教育变革趋势",
            "7. 实拍图：孩子使用AI学习场景"
        ]
        return "\n".join(suggestions)

    def _generate_video_suggestions(self, topic) -> str:
        """生成视频建议"""
        suggestions = [
            "1. 演示视频：实际操作AI工具",
            "2. 对比视频：使用前后效果对比",
            "3. 访谈视频：教育专家观点",
            "4. 教程视频：如何正确使用AI",
            "5. 记录视频：真实学习场景",
            "6. 解说视频：深入浅出讲解",
            "7. 互动视频：问答形式"
        ]
        return "\n".join(suggestions)

    def get_progress(self, batch_id: str) -> Optional[Dict]:
        """获取生成进度"""
        progress = self.progress_store.get(batch_id)
        if progress:
            return progress.to_dict()
        return None

    def get_generated_posts(self, batch_id: str) -> List[ViralPost]:
        """获取生成的爆文"""
        return ViralPostRepository.get_by_batch_id(batch_id)


# 测试代码
if __name__ == '__main__':
    service = GenerateService()

    # 测试生成
    print("=" * 70)
    print("测试爆文生成服务")
    print("=" * 70)

    # 获取最近的话题
    topics = HotTopicRepository.get_available_topics(days=1, limit=3)
    print(f"\n找到 {len(topics)} 个可用话题")

    if topics:
        topic_ids = [t.id for t in topics]
        result = service.generate_viral_posts(
            topic_ids=topic_ids,
            async_execution=False
        )

        print("\n生成结果:")
        print(f"批次ID: {result.get('batch_id')}")
        print(f"状态: {result.get('status')}")
        print(f"总话题数: {result.get('total')}")
        print(f"成功数: {result.get('success')}")
        print(f"失败数: {result.get('failed')}")
        print(f"生成爆文数: {result.get('total_posts')}")
