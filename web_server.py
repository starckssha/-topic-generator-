#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点抓取与爆文生成系统 - Web API服务器
提供完整的REST API和Web页面
"""
import os
import sys
import json
from datetime import datetime

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services import FetchService, GenerateService
from src.database.repositories import (
    HotTopicRepository, ViralPostRepository,
    TaskExecutionRepository, UsedTopicRepository
)
from src.database.connection import test_connection

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# 初始化服务
fetch_service = FetchService()
generate_service = GenerateService()


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/fetch')
def fetch_page():
    """抓取管理页"""
    return render_template('fetch.html')


@app.route('/generate')
def generate_page():
    """生成管理页"""
    return render_template('generate.html')


@app.route('/history')
def history_page():
    """历史查询页"""
    return render_template('history.html')


@app.route('/api/docs')
def api_docs():
    """API文档"""
    return render_template('api_docs.html')


# ==================== 抓取相关API ====================

@app.route('/api/fetch/start', methods=['POST'])
def api_fetch_start():
    """触发抓取任务"""
    try:
        data = request.get_json() or {}
        platforms = data.get('platforms')
        async_exec = data.get('async', True)

        result = fetch_service.fetch_hot_topics(
            platforms=platforms,
            async_execution=async_exec
        )

        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/fetch/progress/<batch_id>')
def api_fetch_progress(batch_id):
    """查询抓取进度"""
    try:
        progress = fetch_service.get_progress(batch_id)
        if progress:
            return jsonify({'status': 'success', 'data': progress})
        else:
            return jsonify({'status': 'error', 'message': '批次ID不存在'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/fetch/results')
def api_fetch_results():
    """获取抓取结果列表"""
    try:
        date = request.args.get('date')
        batch_id = request.args.get('batch_id')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 1000))  # 默认返回1000条，实际上返回所有

        if batch_id:
            topics = HotTopicRepository.get_by_batch_id(batch_id)
        elif date:
            topics = HotTopicRepository.get_by_date(date)
        else:
            topics = HotTopicRepository.get_by_date(datetime.now().strftime('%Y-%m-%d'))

        # 返回所有数据（或者按size限制）
        if size >= 1000:
            # 返回所有数据
            results = [topic.to_dict() for topic in topics]
            return jsonify({
                'status': 'success',
                'data': {
                    'total': len(results),
                    'topics': results
                }
            })
        else:
            # 分页
            start = (page - 1) * size
            end = start + size
            results = [topic.to_dict() for topic in topics[start:end]]
            return jsonify({
                'status': 'success',
                'data': {
                    'total': len(topics),
                    'page': page,
                    'size': size,
                    'topics': results
                }
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== 生成相关API ====================

@app.route('/api/generate/available-topics')
def api_generate_available_topics():
    """获取可生成的话题列表"""
    try:
        days = int(request.args.get('days', 30))
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))

        topics = HotTopicRepository.get_available_topics(days, category, limit)
        results = [topic.to_dict() for topic in topics]

        return jsonify({
            'status': 'success',
            'data': {'total': len(results), 'topics': results}
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/generate/start', methods=['POST'])
def api_generate_start():
    """触发爆文生成任务"""
    try:
        data = request.get_json() or {}
        topic_ids = data.get('topic_ids', [])
        use_ai = data.get('use_ai', False)
        title_types = data.get('title_types')
        async_exec = data.get('async', True)

        if not topic_ids:
            return jsonify({'status': 'error', 'message': '缺少topic_ids参数'}), 400

        result = generate_service.generate_viral_posts(
            topic_ids=topic_ids,
            use_ai=use_ai,
            title_types=title_types,
            async_execution=async_exec
        )

        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/generate/progress/<batch_id>')
def api_generate_progress(batch_id):
    """查询生成进度"""
    try:
        progress = generate_service.get_progress(batch_id)
        if progress:
            return jsonify({'status': 'success', 'data': progress})
        else:
            return jsonify({'status': 'error', 'message': '批次ID不存在'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/generate/posts')
def api_generate_posts():
    """获取生成的爆文列表"""
    try:
        date = request.args.get('date')
        batch_id = request.args.get('batch_id')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))

        if batch_id:
            posts = ViralPostRepository.get_by_batch_id(batch_id)
        elif date:
            posts = ViralPostRepository.get_by_date(date)
        else:
            posts = ViralPostRepository.get_by_date(datetime.now().strftime('%Y-%m-%d'))

        start = (page - 1) * size
        end = start + size
        results = [post.to_dict() for post in posts[start:end]]

        return jsonify({
            'status': 'success',
            'data': {
                'total': len(posts),
                'page': page,
                'size': size,
                'posts': results
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/generate/posts/<int:post_id>')
def api_generate_post_detail(post_id):
    """获取单条爆文详情"""
    try:
        post = ViralPostRepository.get_by_id(post_id)
        if post:
            return jsonify({'status': 'success', 'data': post.to_dict()})
        else:
            return jsonify({'status': 'error', 'message': '爆文不存在'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== 查询相关API ====================

@app.route('/api/history/batches')
def api_history_batches():
    """获取某天的所有抓取批次"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        # 获取该天的所有抓取任务
        fetch_tasks = TaskExecutionRepository.get_by_date_range(date, date, 'fetch_hot_topics')

        # 为每个批次统计数量
        batches = []
        for task in fetch_tasks:
            batch_id = task.batch_id
            # 获取该批次抓取的话题数量
            topics = HotTopicRepository.get_by_batch_id(batch_id)
            # 获取该批次生成的爆文数量
            generate_tasks = TaskExecutionRepository.get_by_batch_id(batch_id, 'generate_viral_posts')
            total_posts = 0
            if generate_tasks:
                for gt in generate_tasks:
                    result = gt.get_result_summary()
                    if isinstance(result, dict):
                        total_posts += result.get('total_posts', 0)

            batches.append({
                'batch_id': batch_id,
                'start_time': task.start_time.strftime('%H:%M:%S') if task.start_time else '',
                'status': task.status,
                'topics_count': len(topics),
                'posts_count': total_posts,
                'duration': task.duration_seconds
            })

        # 按开始时间排序
        batches.sort(key=lambda x: x['start_time'], reverse=True)

        return jsonify({
            'status': 'success',
            'data': {
                'date': date,
                'batches': batches,
                'total_batches': len(batches)
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/history/batch/<batch_id>/data-chain')
def api_history_batch_data_chain(batch_id):
    """获取某个批次的完整数据链路"""
    try:
        # 获取该批次的信息
        fetch_tasks = TaskExecutionRepository.get_by_batch_id(batch_id, 'fetch_hot_topics')
        fetch_task = fetch_tasks[0] if fetch_tasks else None
        hot_topics = HotTopicRepository.get_by_batch_id(batch_id)

        # 获取相关的生成任务
        generate_tasks = []
        viral_posts = []

        # 从hot_topics中找到已生成的话题，获取其爆文
        for topic in hot_topics:
            if topic.first_generated_at:
                # 获取该话题生成的爆文
                posts = ViralPostRepository.get_by_hot_topic_id(topic.id)
                viral_posts.extend(posts)

        # 获取该批次相关的生成任务
        all_generate_tasks = TaskExecutionRepository.get_by_date_range(
            batch_id[:8], batch_id[:8], 'generate_viral_posts'
        )
        generate_tasks = [t for t in all_generate_tasks]

        return jsonify({
            'status': 'success',
            'data': {
                'batch_id': batch_id,
                'fetch_task': fetch_task[0].to_dict() if fetch_task else None,
                'generate_tasks': [task.to_dict() for task in generate_tasks],
                'hot_topics': [topic.to_dict() for topic in hot_topics[:20]],  # 限制20条
                'viral_posts': [post.to_dict() for post in viral_posts[:20]]  # 限制20条
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/history/data-chain')
def api_history_data_chain():
    """按日期查询完整数据链路"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        fetch_tasks = TaskExecutionRepository.get_by_date_range(date, date, 'fetch_hot_topics')
        generate_tasks = TaskExecutionRepository.get_by_date_range(date, date, 'generate_viral_posts')
        hot_topics = HotTopicRepository.get_by_date(date)
        viral_posts = ViralPostRepository.get_by_date(date)

        return jsonify({
            'status': 'success',
            'data': {
                'date': date,
                'fetch_tasks': [task.to_dict() for task in fetch_tasks],
                'generate_tasks': [task.to_dict() for task in generate_tasks],
                'hot_topics': [topic.to_dict() for topic in hot_topics[:10]],
                'viral_posts': [post.to_dict() for post in viral_posts[:10]]
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/stats/overview')
def api_stats_overview():
    """获取统计数据概览"""
    try:
        stats = {
            'total_hot_topics': 0,
            'total_viral_posts': 0,
            'total_fetch_tasks': 0,
            'total_generate_tasks': 0,
            'platform_distribution': HotTopicRepository.get_platform_stats(),
            'used_topics_stats': UsedTopicRepository.get_stats()
        }

        return jsonify({'status': 'success', 'data': stats})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== 系统相关API ====================

@app.route('/api/system/health')
def api_system_health():
    """系统健康检查"""
    try:
        db_status = "connected" if test_connection() else "disconnected"

        return jsonify({
            'status': 'success',
            'data': {
                'database': db_status,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/system/config')
def api_system_config():
    """获取系统配置"""
    try:
        from config import CONFIG

        return jsonify({
            'status': 'success',
            'data': {
                'enabled_platforms': CONFIG.get('enabled_platforms', []),
                'title_types': list(generate_service.TITLE_TEMPLATES.keys())
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== 启动服务 ====================

if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info("=" * 70)
    logger.info("🚀 热点抓取与爆文生成系统")
    logger.info("=" * 70)
    logger.info("📊 主页: http://localhost:5000/")
    logger.info("📥 抓取管理: http://localhost:5000/fetch")
    logger.info("📝 生成管理: http://localhost:5000/generate")
    logger.info("📜 历史查询: http://localhost:5000/history")
    logger.info("=" * 70)
    logger.info("")

    app.run(host='0.0.0.0', port=5000, debug=False)
