"""
数据库初始化脚本
创建数据库表结构并初始化数据
"""
import pymysql
import sys
import os

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据库配置
DB_CONFIG = {
    'host': 'sh-cdb-qkm4h7s0.sql.tencentcdb.com',
    'port': 27339,
    'user': 'root',
    'password': 'sx@123456',
    'database': 'topic_generator',
    'charset': 'utf8mb4'
}


def create_database():
    """创建数据库"""
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        cursor = connection.cursor()

        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ 数据库 `{DB_CONFIG['database']}` 创建成功")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        raise


def create_tables():
    """创建数据库表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # 1. 创建热点话题表
        create_hot_topics_table = """
        CREATE TABLE IF NOT EXISTS `hot_topics` (
          `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
          `title` VARCHAR(500) NOT NULL COMMENT '话题标题',
          `platform` VARCHAR(50) NOT NULL COMMENT '来源平台',
          `rank` INT DEFAULT 0 COMMENT '排名',
          `hot_value` INT DEFAULT 0 COMMENT '热度值',
          `url` VARCHAR(1000) COMMENT '链接地址',
          `category` VARCHAR(50) COMMENT '分类(tech/education/general)',
          `fetched_at` DATETIME NOT NULL COMMENT '抓取时间',
          `batch_id` VARCHAR(50) COMMENT '批次ID',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          INDEX `idx_platform` (`platform`),
          INDEX `idx_fetched_at` (`fetched_at`),
          INDEX `idx_batch_id` (`batch_id`),
          INDEX `idx_category` (`category`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='热点话题表';
        """
        cursor.execute(create_hot_topics_table)
        print("✅ 表 `hot_topics` 创建成功")

        # 2. 创建爆文表
        create_viral_posts_table = """
        CREATE TABLE IF NOT EXISTS `viral_posts` (
          `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
          `hot_topic_id` INT COMMENT '关联的热点话题ID',
          `original_topic` VARCHAR(500) COMMENT '原热点话题',
          `source_platform` VARCHAR(50) COMMENT '来源平台',
          `topic_category` VARCHAR(50) COMMENT '话题分类',
          `title_type` VARCHAR(50) COMMENT '标题类型(震撼型/对比型/数据型/方法型/焦虑共鸣型/前瞻型)',
          `recommended_title` VARCHAR(500) NOT NULL COMMENT '推荐标题',
          `content` TEXT COMMENT '正文内容',
          `image_suggestions` TEXT COMMENT '建议配图',
          `video_suggestions` TEXT COMMENT '建议视频',
          `generated_at` DATETIME NOT NULL COMMENT '生成时间',
          `batch_id` VARCHAR(50) COMMENT '批次ID',
          `is_published` TINYINT DEFAULT 0 COMMENT '是否已发布(0否1是)',
          `published_at` DATETIME COMMENT '发布时间',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          FOREIGN KEY (`hot_topic_id`) REFERENCES `hot_topics`(`id`) ON DELETE SET NULL,
          INDEX `idx_hot_topic_id` (`hot_topic_id`),
          INDEX `idx_generated_at` (`generated_at`),
          INDEX `idx_batch_id` (`batch_id`),
          INDEX `idx_is_published` (`is_published`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爆文表';
        """
        cursor.execute(create_viral_posts_table)
        print("✅ 表 `viral_posts` 创建成功")

        # 3. 创建任务执行记录表
        create_task_executions_table = """
        CREATE TABLE IF NOT EXISTS `task_executions` (
          `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
          `task_type` VARCHAR(50) NOT NULL COMMENT '任务类型(fetch_hot_topics/generate_viral_posts)',
          `batch_id` VARCHAR(50) NOT NULL COMMENT '批次ID',
          `status` VARCHAR(20) NOT NULL COMMENT '状态(running/success/failed)',
          `start_time` DATETIME NOT NULL COMMENT '开始时间',
          `end_time` DATETIME COMMENT '结束时间',
          `duration_seconds` INT COMMENT '执行时长(秒)',
          `result_summary` TEXT COMMENT '结果摘要(JSON格式)',
          `error_message` TEXT COMMENT '错误信息',
          `triggered_by` VARCHAR(50) DEFAULT 'manual' COMMENT '触发方式(manual/scheduled)',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          INDEX `idx_task_type` (`task_type`),
          INDEX `idx_batch_id` (`batch_id`),
          INDEX `idx_status` (`status`),
          INDEX `idx_start_time` (`start_time`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务执行记录表';
        """
        cursor.execute(create_task_executions_table)
        print("✅ 表 `task_executions` 创建成功")

        # 4. 创建已使用话题追踪表
        create_used_topics_table = """
        CREATE TABLE IF NOT EXISTS `used_topics` (
          `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
          `normalized_title` VARCHAR(500) NOT NULL COMMENT '标准化标题',
          `original_title` VARCHAR(500) COMMENT '原始标题',
          `platform` VARCHAR(50) COMMENT '平台',
          `category` VARCHAR(50) COMMENT '分类',
          `url` VARCHAR(1000) COMMENT '链接',
          `used_at` DATETIME NOT NULL COMMENT '使用时间',
          `metadata` TEXT COMMENT '元数据(JSON格式)',
          `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          INDEX `idx_normalized_title` (`normalized_title`),
          INDEX `idx_used_at` (`used_at`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='已使用话题追踪表';
        """
        cursor.execute(create_used_topics_table)
        print("✅ 表 `used_topics` 创建成功")

        connection.commit()
        cursor.close()
        connection.close()

        print("\n🎉 所有数据库表创建完成！")

    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        raise


def show_tables():
    """显示所有表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("\n📋 当前数据库的表：")
        for table in tables:
            print(f"   - {table[0]}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"❌ 查询表失败: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 开始初始化数据库...")
    print("=" * 60)

    try:
        # 1. 创建数据库
        print("\n步骤 1/3: 创建数据库")
        print("-" * 60)
        create_database()

        # 2. 创建表
        print("\n步骤 2/3: 创建数据表")
        print("-" * 60)
        create_tables()

        # 3. 显示所有表
        print("\n步骤 3/3: 验证表结构")
        print("-" * 60)
        show_tables()

        print("\n" + "=" * 60)
        print("✅ 数据库初始化完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        sys.exit(1)
