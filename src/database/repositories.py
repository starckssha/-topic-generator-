"""
数据访问层
提供对数据库的CRUD操作
"""
from datetime import datetime, timedelta
from .connection import get_db
from .models import HotTopic, ViralPost, TaskExecution, UsedTopic


class HotTopicRepository:
    """热点话题数据访问类"""

    @staticmethod
    def insert(topic: HotTopic) -> int:
        """
        插入热点话题

        Args:
            topic: HotTopic实例

        Returns:
            int: 插入的ID
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(topic.insert_query(), topic.to_tuple())
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def batch_insert(topics: list) -> int:
        """
        批量插入热点话题

        Args:
            topics: HotTopic实例列表

        Returns:
            int: 插入的数量
        """
        if not topics:
            return 0

        with get_db() as db:
            cursor = db.cursor()
            tuples = [topic.to_tuple() for topic in topics]
            cursor.executemany(topics[0].insert_query(), tuples)
            db.commit()
            return cursor.rowcount

    @staticmethod
    def get_by_id(topic_id: int) -> HotTopic:
        """
        根据ID获取热点话题

        Args:
            topic_id: 话题ID

        Returns:
            HotTopic: 话题实例
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM hot_topics WHERE id = %s", (topic_id,))
            result = cursor.fetchone()
            if result:
                return HotTopic(**result)
            return None

    @staticmethod
    def get_by_batch_id(batch_id: str, limit: int = None) -> list:
        """
        根据批次ID获取热点话题列表

        Args:
            batch_id: 批次ID
            limit: 限制数量

        Returns:
            list: HotTopic实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT * FROM hot_topics WHERE batch_id = %s ORDER BY hot_value DESC"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query, (batch_id,))
            results = cursor.fetchall()
            return [HotTopic(**result) for result in results]

    @staticmethod
    def get_by_date(date: str, platform: str = None, category: str = None) -> list:
        """
        根据日期获取热点话题列表

        Args:
            date: 日期 (YYYY-MM-DD)
            platform: 平台筛选（可选）
            category: 分类筛选（可选）

        Returns:
            list: HotTopic实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT * FROM hot_topics WHERE DATE(fetched_at) = %s"
            params = [date]

            if platform:
                query += " AND platform = %s"
                params.append(platform)

            if category:
                query += " AND category = %s"
                params.append(category)

            query += " ORDER BY hot_value DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            return [HotTopic(**result) for result in results]

    @staticmethod
    def get_available_topics(days: int = 30, category: str = None, limit: int = None) -> list:
        """
        获取可用的话题（从未生成过爆文的话题）

        Args:
            days: 忽略此参数（保留用于兼容性）
            category: 分类筛选
            limit: 限制数量

        Returns:
            list: HotTopic实例列表
        """
        with get_db() as db:
            cursor = db.cursor()

            # 直接查询从未生成过爆文的话题
            query = "SELECT * FROM hot_topics WHERE first_generated_at IS NULL"
            params = []

            if category:
                query += " AND category = %s"
                params.append(category)

            query += " ORDER BY fetched_at DESC"

            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query, params)
            results = cursor.fetchall()
            return [HotTopic(**result) for result in results]

    @staticmethod
    def mark_as_generated(topic_id: int, generated_at: datetime = None) -> bool:
        """
        标记话题为已生成

        Args:
            topic_id: 话题ID
            generated_at: 生成时间（默认为当前时间）

        Returns:
            bool: 是否成功
        """
        try:
            with get_db() as db:
                cursor = db.cursor()
                if generated_at is None:
                    generated_at = datetime.now()

                cursor.execute("""
                    UPDATE hot_topics
                    SET first_generated_at = %s
                    WHERE id = %s AND first_generated_at IS NULL
                """, (generated_at, topic_id))
                db.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"标记话题失败: {e}")
            return False

    @staticmethod
    def get_platform_stats() -> dict:
        """
        获取各平台的统计数据

        Returns:
            dict: 平台统计
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT platform, COUNT(*) as count
                FROM hot_topics
                GROUP BY platform
            """)
            results = cursor.fetchall()
            return {r['platform']: r['count'] for r in results}


class ViralPostRepository:
    """爆文数据访问类"""

    @staticmethod
    def insert(post: ViralPost) -> int:
        """
        插入爆文

        Args:
            post: ViralPost实例

        Returns:
            int: 插入的ID
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(post.insert_query(), post.to_tuple())
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def batch_insert(posts: list) -> int:
        """
        批量插入爆文

        Args:
            posts: ViralPost实例列表

        Returns:
            int: 插入的数量
        """
        if not posts:
            return 0

        with get_db() as db:
            cursor = db.cursor()
            tuples = [post.to_tuple() for post in posts]
            cursor.executemany(posts[0].insert_query(), tuples)
            db.commit()
            return cursor.rowcount

    @staticmethod
    def get_by_id(post_id: int) -> ViralPost:
        """
        根据ID获取爆文

        Args:
            post_id: 爆文ID

        Returns:
            ViralPost: 爆文实例
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM viral_posts WHERE id = %s", (post_id,))
            result = cursor.fetchone()
            if result:
                return ViralPost(**result)
            return None

    @staticmethod
    def get_by_batch_id(batch_id: str) -> list:
        """
        根据批次ID获取爆文列表

        Args:
            batch_id: 批次ID

        Returns:
            list: ViralPost实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM viral_posts WHERE batch_id = %s", (batch_id,))
            results = cursor.fetchall()
            return [ViralPost(**result) for result in results]

    @staticmethod
    def get_by_date(date: str) -> list:
        """
        根据日期获取爆文列表

        Args:
            date: 日期 (YYYY-MM-DD)

        Returns:
            list: ViralPost实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM viral_posts WHERE DATE(generated_at) = %s ORDER BY generated_at DESC",
                (date,)
            )
            results = cursor.fetchall()
            return [ViralPost(**result) for result in results]

    @staticmethod
    def get_by_hot_topic_id(hot_topic_id: int) -> list:
        """
        根据热点话题ID获取爆文列表

        Args:
            hot_topic_id: 热点话题ID

        Returns:
            list: ViralPost实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM viral_posts WHERE hot_topic_id = %s ORDER BY generated_at DESC",
                (hot_topic_id,)
            )
            results = cursor.fetchall()
            return [ViralPost(**result) for result in results]

    @staticmethod
    def get_unpublished(limit: int = None) -> list:
        """
        获取未发布的爆文

        Args:
            limit: 限制数量

        Returns:
            list: ViralPost实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT * FROM viral_posts WHERE is_published = 0 ORDER BY generated_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
            results = cursor.fetchall()
            return [ViralPost(**result) for result in results]

    @staticmethod
    def mark_as_published(post_id: int):
        """
        标记为已发布

        Args:
            post_id: 爆文ID
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE viral_posts SET is_published = 1, published_at = %s WHERE id = %s",
                (datetime.now(), post_id)
            )
            db.commit()


class TaskExecutionRepository:
    """任务执行记录数据访问类"""

    @staticmethod
    def insert(task: TaskExecution) -> int:
        """
        插入任务记录

        Args:
            task: TaskExecution实例

        Returns:
            int: 插入的ID
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(task.insert_query(), task.to_tuple())
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def update_status(task_id: int, status: str, end_time=None, duration_seconds=None):
        """
        更新任务状态

        Args:
            task_id: 任务ID
            status: 状态
            end_time: 结束时间
            duration_seconds: 执行时长
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "UPDATE task_executions SET status = %s"
            params = [status]

            if end_time:
                query += ", end_time = %s"
                params.append(end_time)

            if duration_seconds:
                query += ", duration_seconds = %s"
                params.append(duration_seconds)

            query += " WHERE id = %s"
            params.append(task_id)

            cursor.execute(query, params)
            db.commit()

    @staticmethod
    def get_by_batch_id(batch_id: str, task_type: str = None) -> list:
        """
        根据批次ID获取任务记录列表

        Args:
            batch_id: 批次ID
            task_type: 任务类型（可选）

        Returns:
            list: TaskExecution实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT * FROM task_executions WHERE batch_id = %s"
            params = [batch_id]

            if task_type:
                query += " AND task_type = %s"
                params.append(task_type)

            cursor.execute(query, params)
            results = cursor.fetchall()
            return [TaskExecution(**result) for result in results]

    @staticmethod
    def get_by_date_range(start_date: str, end_date: str, task_type: str = None) -> list:
        """
        根据日期范围获取任务记录

        Args:
            start_date: 开始日期
            end_date: 结束日期
            task_type: 任务类型筛选

        Returns:
            list: TaskExecution实例列表
        """
        with get_db() as db:
            cursor = db.cursor()
            query = "SELECT * FROM task_executions WHERE DATE(start_time) BETWEEN %s AND %s"
            params = [start_date, end_date]

            if task_type:
                query += " AND task_type = %s"
                params.append(task_type)

            query += " ORDER BY start_time DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            return [TaskExecution(**result) for result in results]


class UsedTopicRepository:
    """已使用话题数据访问类"""

    @staticmethod
    def insert(topic: UsedTopic) -> int:
        """
        插入已使用话题

        Args:
            topic: UsedTopic实例

        Returns:
            int: 插入的ID
        """
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(topic.insert_query(), topic.to_tuple())
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def batch_insert(topics: list) -> int:
        """
        批量插入已使用话题

        Args:
            topics: UsedTopic实例列表

        Returns:
            int: 插入的数量
        """
        if not topics:
            return 0

        with get_db() as db:
            cursor = db.cursor()
            tuples = [topic.to_tuple() for topic in topics]
            cursor.executemany(topics[0].insert_query(), tuples)
            db.commit()
            return cursor.rowcount

    @staticmethod
    def is_topic_used(title: str, days: int = 30) -> bool:
        """
        检查话题是否已使用

        Args:
            title: 话题标题
            days: 天数

        Returns:
            bool: 是否已使用
        """
        normalized_title = UsedTopic.normalize_title(title)
        cutoff_date = datetime.now() - timedelta(days=days)

        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM used_topics
                WHERE normalized_title = %s AND used_at >= %s
            """, (normalized_title, cutoff_date))
            result = cursor.fetchone()
            return result['count'] > 0

    @staticmethod
    def get_stats() -> dict:
        """
        获取使用统计

        Returns:
            dict: 统计数据
        """
        with get_db() as db:
            cursor = db.cursor()

            # 总使用数
            cursor.execute("SELECT COUNT(*) as total FROM used_topics")
            total = cursor.fetchone()['total']

            # 7天内使用数
            cutoff_7days = datetime.now() - timedelta(days=7)
            cursor.execute("SELECT COUNT(*) as count FROM used_topics WHERE used_at >= %s", (cutoff_7days,))
            last_7_days = cursor.fetchone()['count']

            # 30天内使用数
            cutoff_30days = datetime.now() - timedelta(days=30)
            cursor.execute("SELECT COUNT(*) as count FROM used_topics WHERE used_at >= %s", (cutoff_30days,))
            last_30_days = cursor.fetchone()['count']

            return {
                'total': total,
                'last_7_days': last_7_days,
                'last_30_days': last_30_days
            }
