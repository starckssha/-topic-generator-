"""
添加首次生成时间字段
用于追踪话题是否已生成过爆文，避免重复
支持MySQL和PostgreSQL
"""
import os
import sys

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 数据库配置 (从环境变量读取)
DB_TYPE = os.getenv('DB_TYPE', 'postgresql' if os.getenv('RAILWAY_ENVIRONMENT') else 'mysql')

if DB_TYPE == 'postgresql':
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'topic_generator'),
            'cursor_factory': RealDictCursor
        }
    except ImportError:
        print("❌ PostgreSQL驱动未安装，请运行: pip install psycopg2-binary")
        sys.exit(1)
else:
    try:
        import pymysql
        DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'sh-cdb-qkm4h7s0.sql.tencentcdb.com'),
            'port': int(os.getenv('DB_PORT', 27339)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'sx@123456'),
            'database': os.getenv('DB_NAME', 'topic_generator'),
            'charset': 'utf8mb4'
        }
    except ImportError:
        print("❌ MySQL驱动未安装，请运行: pip install pymysql")
        sys.exit(1)


def add_first_generated_at_field():
    """添加first_generated_at字段到hot_topics表"""
    try:
        if DB_TYPE == 'postgresql':
            connection = psycopg2.connect(**DB_CONFIG)
        else:
            connection = pymysql.connect(**DB_CONFIG)

        cursor = connection.cursor()

        # 检查字段是否已存在
        if DB_TYPE == 'postgresql':
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = 'hot_topics'
                AND column_name = 'first_generated_at'
            """)
        else:
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'hot_topics'
                AND COLUMN_NAME = 'first_generated_at'
            """, (DB_CONFIG['database'],))

        if cursor.fetchone():
            print("✅ 字段 first_generated_at 已存在，无需添加")
        else:
            # 添加字段
            if DB_TYPE == 'postgresql':
                alter_sql = """
                    ALTER TABLE hot_topics
                    ADD COLUMN first_generated_at TIMESTAMP
                """
            else:
                alter_sql = """
                    ALTER TABLE hot_topics
                    ADD COLUMN `first_generated_at` DATETIME COMMENT '首次生成爆文时间'
                    AFTER `batch_id`
                """

            cursor.execute(alter_sql)
            connection.commit()
            print("✅ 成功添加字段 first_generated_at")

        # 添加索引
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_first_generated_at
                ON hot_topics(first_generated_at)
            """)
            connection.commit()
            print("✅ 成功添加索引 idx_first_generated_at")
        except Exception as e:
            if "Duplicate key name" in str(e) or "already exists" in str(e):
                print("✅ 索引 idx_first_generated_at 已存在")
            else:
                raise

        cursor.close()
        connection.close()

        print("\n🎉 数据库更新完成！")

    except Exception as e:
        print(f"❌ 更新数据库失败 ({DB_TYPE}): {e}")
        raise


if __name__ == '__main__':
    print("=" * 60)
    print(f"  添加首次生成时间字段 ({DB_TYPE.upper()})")
    print("=" * 60)
    print(f"数据库类型: {DB_TYPE}")
    print(f"数据库主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print()

    add_first_generated_at_field()
