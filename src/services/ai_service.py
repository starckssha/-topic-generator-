"""
DeepSeek AI增强服务
使用DeepSeek R1模型增强爆文生成（同步版本）
"""
import os
import requests
import json
from typing import List, Dict, Optional

# DeepSeek API配置
DEEPSEEK_CONFIG = {
    'api_url': 'http://ai-api.applesay.cn/v1/chat/completions',
    'api_key': 'sk-aXWs0YDBq79J7Xx59aD6993bCa4e4a86813eE2Fa1eFd110d',
    'model': 'deepseek-r1',
    'timeout': 60
}


class AIService:
    """DeepSeek AI增强服务类（同步版本）"""

    def __init__(self, api_key: str = None):
        """
        初始化AI服务

        Args:
            api_key: API密钥，默认使用配置中的密钥
        """
        self.api_url = DEEPSEEK_CONFIG['api_url']
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY', DEEPSEEK_CONFIG['api_key'])
        self.model = DEEPSEEK_CONFIG['model']
        self.timeout = DEEPSEEK_CONFIG['timeout']

    def enhance_title(
        self,
        original_title: str,
        topic: str,
        platform: str,
        title_type: str = '震撼型',
        count: int = 3
    ) -> List[Dict]:
        """
        AI增强标题生成

        Args:
            original_title: 原始标题
            topic: 话题内容
            platform: 来源平台
            title_type: 标题类型
            count: 生成数量

        Returns:
            标题列表
        """
        prompt = f"""
你是一位小红书爆款内容创作专家。基于以下热点话题，生成{count}个吸引眼球的标题。

话题：{topic}
来源平台：{platform}
原始标题：{original_title}
标题类型：{title_type}

要求：
1. 标题要吸引眼球，适合小红书平台
2. 添加适当的emoji表情（如🔥、⚠️、✨、💡等）
3. 标题长度在20-40字之间
4. 符合"{title_type}"的风格特点
5. 标题要能引起目标用户的共鸣或好奇心

请直接返回{count}个标题，每行一个，不要添加序号或其他标记。
"""

        try:
            response = self._call_api(prompt)
            titles = self._parse_titles(response)
            return [{'type': title_type, 'title': title} for title in titles]
        except Exception as e:
            print(f"AI标题生成失败: {e}")
            return []

    def enhance_content(
        self,
        topic: str,
        title: str,
        title_type: str
    ) -> str:
        """
        AI增强内容生成

        Args:
            topic: 话题内容
            title: 标题
            title_type: 标题类型

        Returns:
            增强后的内容
        """
        prompt = f"""
你是一位小红书爆款内容创作专家。基于以下信息，生成一篇完整的小红书笔记。

话题：{topic}
标题：{title}
内容类型：{title_type}

要求：
1. 内容要符合小红书平台风格（口语化、接地气、有亲和力）
2. 结构清晰，分段明确（使用emoji作为段落标记）
3. 长度在500-800字之间
4. 包含具体的信息、数据或案例
5. 结尾添加相关话题标签（5-8个，以#开头）
6. 语气要根据"{title_type}"调整（如震撼型要强烈，方法型要实用）
7. 内容要有价值，能引起读者共鸣或提供实用信息

请直接生成内容，不要添加标题或其他说明。
"""

        try:
            content = self._call_api(prompt)
            return content.strip()
        except Exception as e:
            print(f"AI内容生成失败: {e}")
            return ""

    def generate_hashtags(self, content: str, count: int = 8) -> List[str]:
        """
        生成相关标签

        Args:
            content: 内容文本
            count: 生成数量

        Returns:
            标签列表
        """
        prompt = f"""
基于以下内容，生成{count}个适合小红书的热门话题标签。

内容：{content[:500]}

要求：
1. 标签要与小红书平台相关
2. 标签要有一定的热度
3. 标签格式：#标签名
4. 直接返回{count}个标签，用空格分隔
"""

        try:
            response = self._call_api(prompt)
            hashtags = response.strip().split()
            return hashtags[:count]
        except Exception as e:
            print(f"AI标签生成失败: {e}")
            return ['#AI教育', '#未来教育', '#学习方法', '#干货分享']

    def optimize_post(
        self,
        title: str,
        content: str
    ) -> Dict[str, str]:
        """
        优化完整的爆文

        Args:
            title: 标题
            content: 内容

        Returns:
            优化后的标题和内容
        """
        prompt = f"""
你是一位小红书爆款内容优化专家。请优化以下小红书笔记，使其更具吸引力和传播力。

原标题：{title}
原内容：{content}

优化要求：
1. 标题要更吸引眼球，添加emoji
2. 内容要更口语化、更有亲和力
3. 优化段落结构，使用emoji标记
4. 添加更多实用信息或观点
5. 优化话题标签，选择更热门的标签

请按以下格式返回：
【标题】
优化后的标题

【内容】
优化后的内容
"""

        try:
            response = self._call_api(prompt)
            return self._parse_optimized_post(response)
        except Exception as e:
            print(f"AI优化失败: {e}")
            return {'title': title, 'content': content}

    def generate_content_for_topic(
        self,
        topic_title: str,
        platform: str,
        category: str,
        style: str,
        title_type: str
    ) -> str:
        """
        根据话题生成内容

        Args:
            topic_title: 话题标题
            platform: 平台
            category: 分类
            style: 内容风格要求
            title_type: 标题类型

        Returns:
            生成的内容
        """
        prompt = f"""
你是一位小红书爆款内容创作专家。基于以下热点话题，生成一篇高质量的小红书笔记。

话题：{topic_title}
来源平台：{platform}
话题分类：{category}
内容风格：{style}
标题类型：{title_type}

创作要求：
1. 内容要深度分析这个话题，不能只是简单重复标题
2. 要有具体的信息、数据、案例或观点
3. 结构要清晰，使用emoji作为段落标记
4. 语气要符合小红书风格（口语化、接地气、有亲和力）
5. 长度在600-1000字之间
6. 根据话题特点，提供有价值的见解或实用建议
7. 结尾添加8-10个相关话题标签

请直接生成内容，不要添加标题或其他说明。
"""

        try:
            response = self._call_api(prompt)
            return response.strip()
        except Exception as e:
            print(f"AI生成内容失败: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            # 返回基础内容
            return f"""基于"{topic_title}"的深度分析

📌 {platform}平台热议话题

这个话题反映了{category}领域的重要趋势：

💡 核心观点：
1. 这是一个值得关注的趋势
2. 对教育领域有重要影响
3. 我们需要深入了解和思考

🎯 见解和建议：
✅ 拥抱变化，积极适应
✅ 保持学习和探索的态度
✅ 培养核心竞争力

#AI教育 #教育变革 #未来教育 #学习方法 #干货分享"""

    def _call_api(self, prompt: str) -> str:
        """
        调用DeepSeek API（同步）

        Args:
            prompt: 提示词

        Returns:
            API响应内容
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()

        # 提取返回的文本
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            raise Exception("API返回格式错误")

    def _parse_titles(self, response: str) -> List[str]:
        """解析标题响应"""
        titles = []
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            # 移除序号
            if line and len(line) > 5:
                # 去除可能的序号前缀
                line = line.lstrip('0123456789.-、·.')
                line = line.strip()
                if line:
                    titles.append(line)
        return titles

    def _parse_optimized_post(self, response: str) -> Dict[str, str]:
        """解析优化后的文章"""
        title = ""
        content = ""
        current_section = None

        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if '【标题】' in line:
                current_section = 'title'
            elif '【内容】' in line:
                current_section = 'content'
            elif line:
                if current_section == 'title':
                    title += line + '\n'
                elif current_section == 'content':
                    content += line + '\n'

        return {
            'title': title.strip(),
            'content': content.strip()
        }


# 为了向后兼容，保留SyncAIService别名
SyncAIService = AIService


# 测试代码
if __name__ == '__main__':
    print("=" * 70)
    print("测试DeepSeek AI服务")
    print("=" * 70)

    service = AIService()

    # 测试内容生成
    print("\n测试内容生成...")
    content = service.generate_content_for_topic(
        topic_title="ChatGPT在教育中的应用",
        platform="Hacker News",
        category="AI变革",
        style="写一篇小红书震撼型内容",
        title_type="震撼型"
    )

    print(f"生成的内容长度: {len(content)} 字符")
    print(f"内容预览: {content[:300]}...")
