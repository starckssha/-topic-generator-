#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试HotTopic模型创建"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("测试HotTopic模型")
print("=" * 70)

# 1. 测试导入模型
print("\n[1] 导入HotTopic模型...")
try:
    from src.database.models import HotTopic
    print("✅ 导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 2. 检查__init__参数
print("\n[2] 检查__init__参数...")
import inspect
sig = inspect.signature(HotTopic.__init__)
params = list(sig.parameters.keys())
print(f"✅ 参数列表: {params}")

# 3. 测试创建对象
print("\n[3] 测试创建HotTopic对象...")
test_data = {
    'id': 1,
    'title': 'Test Topic',
    'platform': 'Test Platform',
    'rank': 1,
    'hot_value': 100,
    'url': 'http://test.com',
    'category': 'tech',
    'fetched_at': None,
    'batch_id': 'test_batch',
    'first_generated_at': None,
    'created_at': None
}

try:
    topic = HotTopic(**test_data)
    print(f"✅ 创建成功!")
    print(f"   标题: {topic.title}")
    print(f"   平台: {topic.platform}")
    print(f"   first_generated_at: {topic.first_generated_at}")
except Exception as e:
    print(f"❌ 创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 测试数据库查询
print("\n[4] 测试从数据库查询...")
try:
    from src.database.connection import get_db

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hot_topics LIMIT 1")
        result = cursor.fetchone()

        if result:
            print(f"✅ 查询成功!")
            print(f"   字段: {list(result.keys())}")

            print("\n[5] 使用数据库数据创建HotTopic...")
            try:
                topic = HotTopic(**result)
                print(f"✅ 创建成功!")
                print(f"   标题: {topic.title[:50]}...")
            except Exception as e:
                print(f"❌ 创建失败: {e}")
                print("\n数据库字段 vs 模型参数对比:")
                print(f"  数据库字段: {list(result.keys())}")
                print(f"  模型参数: {params}")

                # 找出不匹配的字段
                db_fields = set(result.keys())
                model_params = set([p for p in params if p != 'self'])
                extra_fields = db_fields - model_params
                missing_fields = model_params - db_fields

                if extra_fields:
                    print(f"  数据库多出的字段: {extra_fields}")
                if missing_fields:
                    print(f"  模型缺少的字段: {missing_fields}")
        else:
            print("⚠️  数据库中没有数据")

except Exception as e:
    print(f"❌ 数据库查询失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
