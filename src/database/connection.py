"""
数据库连接管理 - 支持MySQL和PostgreSQL
"""
from contextlib import contextmanager
import os

# 数据库类型自动检测
DB_TYPE = os.getenv('DB_TYPE', 'postgresql' if os.getenv('RAILWAY_ENVIRONMENT') else 'mysql')

# 根据数据库类型导入相应模块
if DB_TYPE == 'postgresql':
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        POSTGRESQL_AVAILABLE = True
    except ImportError:
        POSTGRESQL_AVAILABLE = False
        print("⚠️ PostgreSQL驱动未安装，请运行: pip install psycopg2-binary")
else:
    try:
        import pymysql
        MYSQL_AVAILABLE = True
    except ImportError:
        MYSQL_AVAILABLE = False
        print("⚠️ MySQL驱动未安装，请运行: pip install pymysql")


# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'sh-cdb-qkm4h7s0.sql.tencentcdb.com'),
    'port': int(os.getenv('DB_PORT', '5432' if DB_TYPE == 'postgresql' else '27339')),
    'user': os.getenv('DB_USER', 'postgres' if DB_TYPE == 'postgresql' else 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'topic_generator'),
}

# PostgreSQL额外配置
if DB_TYPE == 'postgresql':
    DB_CONFIG['cursor_factory'] = RealDictCursor


def get_connection():
    """
    获取数据库连接

    Returns:
        Connection: 数据库连接对象
    """
    try:
        if DB_TYPE == 'postgresql':
            if not POSTGRESQL_AVAILABLE:
                raise ImportError("PostgreSQL driver not available")
            connection = psycopg2.connect(**DB_CONFIG)
        else:
            if not MYSQL_AVAILABLE:
                raise ImportError("MySQL driver not available")
            # MySQL需要额外配置
            mysql_config = DB_CONFIG.copy()
            mysql_config['charset'] = 'utf8mb4'
            mysql_config['cursorclass'] = pymysql.cursors.DictCursor
            connection = pymysql.connect(**mysql_config)

        return connection
    except Exception as e:
        print(f"❌ 数据库连接失败 ({DB_TYPE}): {e}")
        print(f"   配置: host={DB_CONFIG['host']}, port={DB_CONFIG['port']}, db={DB_CONFIG['database']}")
        raise


@contextmanager
def get_db():
    """
    获取数据库连接的上下文管理器

    Usage:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM hot_topics")
            results = cursor.fetchall()
    """
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"❌ 数据库操作失败: {e}")
        raise
    finally:
        connection.close()


@contextmanager
def get_db_session():
    """
    获取数据库会话的上下文管理器
    用于更复杂的数据库操作

    Usage:
        with get_db_session() as session:
            results = session.query(HotTopic).all()
    """
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"❌ 数据库操作失败: {e}")
        raise
    finally:
        connection.close()


def test_connection():
    """
    测试数据库连接

    Returns:
        bool: 连接是否成功
    """
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        return False


if __name__ == '__main__':
    print("🔍 测试数据库连接...")
    if test_connection():
        print("✅ 数据库连接成功")
    else:
        print("❌ 数据库连接失败")
