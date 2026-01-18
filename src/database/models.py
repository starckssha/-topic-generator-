"""
ORM模型定义
"""
from datetime import datetime
import json


class BaseModel:
    """基础模型类"""

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建模型实例

        Args:
            data: 字典数据

        Returns:
            模型实例
        """
        return cls(**data)

    def to_dict(self):
        """
        将模型转换为字典

        Returns:
            dict: 字典数据
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result


class HotTopic(BaseModel):
    """热点话题模型"""

    def __init__(self, id=None, title=None, platform=None, rank=0,
                 hot_value=0, url=None, category=None, fetched_at=None,
                 batch_id=None, first_generated_at=None, created_at=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.rank = rank
        self.hot_value = hot_value
        self.url = url
        self.category = category
        self.fetched_at = fetched_at
        self.batch_id = batch_id
        self.first_generated_at = first_generated_at
        self.created_at = created_at

    @staticmethod
    def table_name():
        return 'hot_topics'

    @staticmethod
    def insert_query():
        return """
            INSERT INTO hot_topics
            (title, platform, `rank`, hot_value, url, category, fetched_at, batch_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

    def to_tuple(self):
        """转换为元组用于插入"""
        return (
            self.title,
            self.platform,
            self.rank,
            self.hot_value,
            self.url,
            self.category,
            self.fetched_at,
            self.batch_id
        )


class ViralPost(BaseModel):
    """爆文模型"""

    def __init__(self, id=None, hot_topic_id=None, original_topic=None,
                 source_platform=None, topic_category=None, title_type=None,
                 recommended_title=None, content=None, image_suggestions=None,
                 video_suggestions=None, generated_at=None, batch_id=None,
                 is_published=0, published_at=None, created_at=None):
        self.id = id
        self.hot_topic_id = hot_topic_id
        self.original_topic = original_topic
        self.source_platform = source_platform
        self.topic_category = topic_category
        self.title_type = title_type
        self.recommended_title = recommended_title
        self.content = content
        self.image_suggestions = image_suggestions
        self.video_suggestions = video_suggestions
        self.generated_at = generated_at
        self.batch_id = batch_id
        self.is_published = is_published
        self.published_at = published_at
        self.created_at = created_at

    @staticmethod
    def table_name():
        return 'viral_posts'

    @staticmethod
    def insert_query():
        return """
            INSERT INTO viral_posts
            (hot_topic_id, original_topic, source_platform, topic_category,
             title_type, recommended_title, content, image_suggestions,
             video_suggestions, generated_at, batch_id, is_published)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def to_tuple(self):
        """转换为元组用于插入"""
        return (
            self.hot_topic_id,
            self.original_topic,
            self.source_platform,
            self.topic_category,
            self.title_type,
            self.recommended_title,
            self.content,
            self.image_suggestions,
            self.video_suggestions,
            self.generated_at,
            self.batch_id,
            self.is_published
        )


class TaskExecution(BaseModel):
    """任务执行记录模型"""

    def __init__(self, id=None, task_type=None, batch_id=None, status=None,
                 start_time=None, end_time=None, duration_seconds=None,
                 result_summary=None, error_message=None, triggered_by='manual',
                 created_at=None):
        self.id = id
        self.task_type = task_type
        self.batch_id = batch_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.duration_seconds = duration_seconds
        self.result_summary = result_summary
        self.error_message = error_message
        self.triggered_by = triggered_by
        self.created_at = created_at

    @staticmethod
    def table_name():
        return 'task_executions'

    @staticmethod
    def insert_query():
        return """
            INSERT INTO task_executions
            (task_type, batch_id, status, start_time, end_time,
             duration_seconds, result_summary, error_message, triggered_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def to_tuple(self):
        """转换为元组用于插入"""
        return (
            self.task_type,
            self.batch_id,
            self.status,
            self.start_time,
            self.end_time,
            self.duration_seconds,
            json.dumps(self.result_summary) if isinstance(self.result_summary, dict) else self.result_summary,
            self.error_message,
            self.triggered_by
        )

    def set_result_summary(self, data):
        """设置结果摘要（自动转换为JSON）"""
        if isinstance(data, dict):
            self.result_summary = json.dumps(data, ensure_ascii=False)
        else:
            self.result_summary = data

    def get_result_summary(self):
        """获取结果摘要（自动解析JSON）"""
        if isinstance(self.result_summary, str):
            try:
                return json.loads(self.result_summary)
            except:
                return self.result_summary
        return self.result_summary


class UsedTopic(BaseModel):
    """已使用话题模型"""

    def __init__(self, id=None, normalized_title=None, original_title=None,
                 platform=None, category=None, url=None, used_at=None,
                 metadata=None, created_at=None):
        self.id = id
        self.normalized_title = normalized_title
        self.original_title = original_title
        self.platform = platform
        self.category = category
        self.url = url
        self.used_at = used_at
        self.metadata = metadata
        self.created_at = created_at

    @staticmethod
    def table_name():
        return 'used_topics'

    @staticmethod
    def insert_query():
        return """
            INSERT INTO used_topics
            (normalized_title, original_title, platform, category, url, used_at, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    def to_tuple(self):
        """转换为元组用于插入"""
        return (
            self.normalized_title,
            self.original_title,
            self.platform,
            self.category,
            self.url,
            self.used_at,
            json.dumps(self.metadata, ensure_ascii=False) if isinstance(self.metadata, dict) else self.metadata
        )

    @staticmethod
    def normalize_title(title):
        """
        标准化标题

        Args:
            title: 原始标题

        Returns:
            str: 标准化后的标题
        """
        if not title:
            return ""
        # 转小写
        title = title.lower()
        # 去除空格
        title = title.replace(" ", "")
        # 去除标点
        import re
        title = re.sub(r'[^\w\u4e00-\u9fff]', '', title)
        return title
