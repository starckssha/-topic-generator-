#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书爆文发布系统 - 后端API服务
提供爆文数据、签名生成、图片服务
"""
import os
import sys
import json
import csv
import time
import hashlib
import random
import string
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import requests

# 设置编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__, template_folder='templates')
CORS(app)  # 允许跨域

# 配置
CONFIG = {
    'CSV_DIR': os.path.join(os.path.dirname(__file__), 'output'),
    'IMAGE_DIR': os.path.join(os.path.dirname(__file__), 'static', 'images'),
    'XHS_APP_KEY': os.getenv('XHS_APP_KEY', 'your_app_key_here'),  # 从环境变量读取
    'XHS_APP_SECRET': os.getenv('XHS_APP_SECRET', 'your_app_secret_here'),
    'XHS_ACCESS_TOKEN': None,
    'XHS_TOKEN_EXPIRES': 0,
    # 公司API配置
    'COMPANY_API_URL': os.getenv('COMPANY_API_URL', 'http://contenthub-test.applesay.cn/app-api/hotword/note-review/create'),
    'COMPANY_API_ENABLED': True  # 是否启用公司API
}

# 确保图片目录存在
os.makedirs(CONFIG['IMAGE_DIR'], exist_ok=True)


def generate_nonce(length=32):
    """生成随机字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_xhs_signature(app_key, nonce, timestamp, secret):
    """
    生成小红书签名

    Args:
        app_key: 应用Key
        nonce: 随机字符串
        timestamp: 时间戳
        secret: 应用密钥或access_token

    Returns:
        签名字符串
    """
    # 参数排序并拼接
    params = {
        'appKey': app_key,
        'nonce': nonce,
        'timeStamp': str(timestamp)
    }

    sorted_params = '&'.join([f"{k}={params[k]}" for k in sorted(params.keys())])
    string_to_sign = sorted_params + secret

    # SHA256加密
    signature = hashlib.sha256(string_to_sign.encode('utf-8')).hexdigest()
    return signature


def get_xhs_access_token():
    """
    获取小红书access_token（带缓存）

    Returns:
        access_token或None
    """
    # 如果使用测试key，返回模拟token
    if CONFIG['XHS_APP_KEY'] == 'your_app_key_here':
        return 'mock_access_token_for_testing'

    # 检查缓存
    if (CONFIG['XHS_ACCESS_TOKEN'] and
        time.time() < CONFIG['XHS_TOKEN_EXPIRES']):
        return CONFIG['XHS_ACCESS_TOKEN']

    # 生成新的签名
    nonce = generate_nonce()
    timestamp = int(time.time())

    signature = generate_xhs_signature(
        CONFIG['XHS_APP_KEY'],
        nonce,
        timestamp,
        CONFIG['XHS_APP_SECRET']
    )

    # 这里应该调用小红书API获取token
    # 由于没有真实API，返回模拟数据
    CONFIG['XHS_ACCESS_TOKEN'] = 'mock_access_token'
    CONFIG['XHS_TOKEN_EXPIRES'] = time.time() + 7200  # 2小时后过期

    return CONFIG['XHS_ACCESS_TOKEN']


@app.route('/')
def index():
    """主页"""
    return """
    <h1>🔥 小红书爆文发布系统 API</h1>
    <p>API接口文档：</p>
    <ul>
        <li><a href="/api/posts">GET /api/posts - 获取爆文列表</a></li>
        <li><a href="/api/posts/{id}">GET /api/posts/{id} - 获取单条爆文</a></li>
        <li><a href="/api/signature">POST /api/signature - 生成分享签名</a></li>
        <li><a href="/api/config">GET /api/config - 获取配置信息</a></li>
        <li><a href="/static/images">图片服务器</a></li>
    </ul>
    <p><a href="/h5/index.html">📱 前端H5页面</a></p>
    """


@app.route('/api/config')
def get_config():
    """获取配置信息"""
    return jsonify({
        'status': 'success',
        'data': {
            'has_xhs_credentials': CONFIG['XHS_APP_KEY'] != 'your_app_key_here',
            'image_server': f'{request.host_url}/static/images/',
            'api_version': '1.0.0'
        }
    })


@app.route('/api/dates')
def get_available_dates():
    """获取所有可用的日期列表"""
    try:
        # 查找所有CSV文件
        csv_files = [f for f in os.listdir(CONFIG['CSV_DIR']) if f.startswith('xiaohongshu_posts_') and f.endswith('.csv')]

        if not csv_files:
            return jsonify({
                'status': 'success',
                'data': {
                    'dates': []
                }
            })

        # 提取日期（格式：xiaohongshu_posts_20260110_143510.csv -> 20260110）
        dates = set()
        for filename in csv_files:
            # 文件名格式：xiaohongshu_posts_YYYYMMDD_HHMMSS.csv
            parts = filename.replace('xiaohongshu_posts_', '').replace('.csv', '').split('_')
            if len(parts) >= 1:
                dates.add(parts[0])

        # 转换为列表并排序（降序）
        sorted_dates = sorted(list(dates), reverse=True)

        # 格式化日期
        formatted_dates = []
        for date_str in sorted_dates:
            if len(date_str) == 8:
                # 转换为更友好的格式：20260110 -> 2026-01-10
                formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                formatted_dates.append({
                    'value': date_str,
                    'label': formatted
                })

        return jsonify({
            'status': 'success',
            'data': {
                'dates': formatted_dates,
                'total': len(formatted_dates)
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/posts')
def get_posts():
    """获取爆文列表"""
    try:
        # 获取日期参数（可选）
        date = request.args.get('date')  # 格式: 20260110

        # 查找CSV文件
        csv_files = [f for f in os.listdir(CONFIG['CSV_DIR']) if f.startswith('xiaohongshu_posts_') and f.endswith('.csv')]

        if not csv_files:
            return jsonify({
                'status': 'error',
                'message': '未找到爆文数据文件'
            }), 404

        # 如果指定了日期，筛选该日期的文件
        if date:
            matched_files = [f for f in csv_files if date in f]
            if not matched_files:
                return jsonify({
                    'status': 'error',
                    'message': f'未找到日期 {date} 的爆文数据'
                }), 404
            csv_path = os.path.join(CONFIG['CSV_DIR'], matched_files[-1])
        else:
            # 按时间排序，取最新的
            latest_file = sorted(csv_files)[-1]
            csv_path = os.path.join(CONFIG['CSV_DIR'], latest_file)

        # 读取CSV
        df = pd.read_csv(csv_path, encoding='utf-8-sig')

        # 转换为JSON
        posts = []
        for idx, row in df.iterrows():
            posts.append({
                'id': idx + 1,
                'original_topic': row.get('原热点话题', ''),
                'platform': row.get('来源平台', ''),
                'category': row.get('话题分类', ''),
                'title_type': row.get('标题类型', ''),
                'title': row.get('推荐标题', ''),
                'content': row.get('正文内容', ''),
                'image_suggestions': row.get('建议配图', ''),
                'video_suggestions': row.get('建议视频', ''),
                'timestamp': row.get('生成时间', '')
            })

        return jsonify({
            'status': 'success',
            'data': {
                'total': len(posts),
                'source_file': os.path.basename(csv_path),
                'posts': posts
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/posts/<int:post_id>')
def get_post(post_id):
    """获取单条爆文"""
    try:
        # 确保 post_id 是整数
        post_id = int(post_id)

        # 获取日期参数（可选）
        date = request.args.get('date')  # 格式: 20260110

        # 获取所有爆文
        csv_files = [f for f in os.listdir(CONFIG['CSV_DIR']) if f.startswith('xiaohongshu_posts_') and f.endswith('.csv')]

        if not csv_files:
            return jsonify({'status': 'error', 'message': '未找到爆文数据'}), 404

        # 如果指定了日期，筛选该日期的文件
        if date:
            matched_files = [f for f in csv_files if date in f]
            if not matched_files:
                return jsonify({'status': 'error', 'message': f'未找到日期 {date} 的爆文数据'}), 404
            csv_path = os.path.join(CONFIG['CSV_DIR'], matched_files[-1])
        else:
            # 按时间排序，取最新的
            latest_file = sorted(csv_files)[-1]
            csv_path = os.path.join(CONFIG['CSV_DIR'], latest_file)

        df = pd.read_csv(csv_path, encoding='utf-8-sig')

        if post_id < 1 or post_id > len(df):
            return jsonify({'status': 'error', 'message': '爆文不存在'}), 404

        row = df.iloc[post_id - 1]

        return jsonify({
            'status': 'success',
            'data': {
                'id': post_id,
                'original_topic': row.get('原热点话题', ''),
                'platform': row.get('来源平台', ''),
                'category': row.get('话题分类', ''),
                'title_type': row.get('标题类型', ''),
                'title': row.get('推荐标题', ''),
                'content': row.get('正文内容', ''),
                'image_suggestions': row.get('建议配图', ''),
                'video_suggestions': row.get('建议视频', ''),
                'timestamp': row.get('生成时间', '')
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """
    生成文章配图（优先使用 Google Nano Banana）

    请求体:
    {
        "title": "文章标题",
        "content": "文章内容" (可选)
    }
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')

        if not title:
            return jsonify({
                'status': 'error',
                'message': '缺少title参数'
            }), 400

        # 导入 Nano Banana 图片生成模块
        sys.path.insert(0, os.path.dirname(__file__))
        from nano_banana_generator import generate_image_with_fallback

        # 生成图片（优先使用 Nano Banana，失败则使用占位图）
        image_url = generate_image_with_fallback(title, content)

        return jsonify({
            'status': 'success',
            'data': {
                'image_url': image_url,
                'title': title,
                'method': 'nano_banana' if 'nano_banana' in image_url else 'placeholder'
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'图片生成失败: {str(e)}'
        }), 500


@app.route('/api/signature', methods=['POST'])
def generate_signature():
    """
    生成小红书分享签名

    请求体:
    {
        "app_key": "xxx"  // 可选，不传则使用默认配置
    }
    """
    try:
        data = request.get_json() or {}
        app_key = data.get('app_key') or CONFIG['XHS_APP_KEY']

        # 生成签名参数
        nonce = generate_nonce()
        timestamp = int(time.time())

        # 获取access_token
        access_token = get_xhs_access_token()

        # 生成签名
        signature = generate_xhs_signature(
            app_key,
            nonce,
            timestamp,
            access_token
        )

        return jsonify({
            'status': 'success',
            'data': {
                'appKey': app_key,
                'nonce': nonce,
                'timestamp': timestamp,
                'signature': signature,
                'expires_in': 7200  # 2小时
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/publish-to-company', methods=['POST'])
def publish_to_company():
    """
    发布到公司API

    请求体:
    {
        "post_id": 1,  // 爆文ID
        "date": "20260110",  // 可选，日期参数
        "generate_image": true,  // 是否生成配图
        "images": ["url1", "url2"]  // 可选，自定义图片URL列表
    }
    """
    try:
        if not CONFIG['COMPANY_API_ENABLED']:
            return jsonify({
                'status': 'error',
                'message': '公司API未启用'
            }), 400

        data = request.get_json()
        if not data:
            data = {}

        post_id = data.get('post_id')
        if not post_id:
            return jsonify({
                'status': 'error',
                'message': '缺少post_id参数'
            }), 400

        # 确保 post_id 是整数
        try:
            post_id = int(post_id)
        except (TypeError, ValueError):
            return jsonify({
                'status': 'error',
                'message': 'post_id参数必须是整数'
            }), 400

        # 获取日期参数（可选）
        date = data.get('date')

        # 获取爆文数据
        csv_files = [f for f in os.listdir(CONFIG['CSV_DIR']) if f.startswith('xiaohongshu_posts_') and f.endswith('.csv')]
        if not csv_files:
            return jsonify({'status': 'error', 'message': '未找到爆文数据'}), 404

        # 如果指定了日期，筛选该日期的文件
        if date:
            matched_files = [f for f in csv_files if date in f]
            if not matched_files:
                return jsonify({'status': 'error', 'message': f'未找到日期 {date} 的爆文数据'}), 404
            csv_path = os.path.join(CONFIG['CSV_DIR'], matched_files[-1])
        else:
            # 按时间排序，取最新的
            latest_file = sorted(csv_files)[-1]
            csv_path = os.path.join(CONFIG['CSV_DIR'], latest_file)

        df = pd.read_csv(csv_path, encoding='utf-8-sig')

        if post_id < 1 or post_id > len(df):
            return jsonify({'status': 'error', 'message': '爆文不存在'}), 404

        row = df.iloc[post_id - 1]

        # 提取标签（从内容中提取hashtag）
        content = row.get('正文内容', '')
        title = row.get('推荐标题', '')

        # 提取hashtags
        import re
        hashtags = re.findall(r'#(\w+)', content)
        tags = ','.join(hashtags) if hashtags else 'AI教育,海外教育,干货分享'

        # 清理标题和内容
        title_clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、％💡🔥⚠️✨💔🤔📊📚🚀💪❤️😱😭🙏🌟🎯📱🎓🇺🇸🌍🤖💻 ]', '', title)
        content_clean = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、％\s\n💡🔥⚠️✨💔🤔📊📚🚀💪❤️😱😭🙏🌟🎯📱🎓🇺🇸🌍🤖💻()]', '', content)

        # 生成或获取图片URL
        image_urls = []

        # 如果用户提供了自定义图片URL
        if data.get('images') and isinstance(data.get('images'), list):
            image_urls = data['images']
        # 如果需要生成图片
        elif data.get('generate_image') is True:
            # 导入图片生成模块
            sys.path.insert(0, os.path.dirname(__file__))
            from image_generator import generate_image_for_post

            # 生成图片（不使用print避免I/O错误）
            image_url = generate_image_for_post(title_clean, content_clean, method='placeholder')
            if image_url:
                image_urls = [image_url]

        # 构造请求数据
        payload = {
            "title": title_clean,
            "content": content_clean,
            "tags": tags,
            "noteImage": ','.join(image_urls) if image_urls else ""
        }

        # 调用公司API
        response = requests.post(
            CONFIG['COMPANY_API_URL'],
            headers={
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )

        # 返回结果
        if response.status_code == 200:
            result = response.json() if response.content else {}
            return jsonify({
                'status': 'success',
                'message': '发布成功',
                'data': {
                    'post_id': post_id,
                    'image_urls': image_urls,
                    'company_response': result
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'发布失败: HTTP {response.status_code}',
                'data': {
                    'response': response.text
                }
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            'status': 'error',
            'message': '请求超时，请检查网络连接'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'发布出错: {str(e)}'
        }), 500


@app.route('/manager')
def manager_page():
    """PC管理页面 - 显示所有爆文和二维码"""
    from flask import render_template
    return render_template('manager.html')


@app.route('/mobile/<int:post_id>')
def mobile_page(post_id):
    """移动端发布页面 - 扫码后打开"""
    from flask import render_template
    return render_template('mobile.html')


@app.route('/static/images/<filename>')
def serve_image(filename):
    """提供图片服务"""
    return send_from_directory(CONFIG['IMAGE_DIR'], filename)


if __name__ == '__main__':
    print("="*70)
    print("🚀 爆文内容发布系统 - 后端服务")
    print("="*70)
    print()
    print("服务地址: http://localhost:5000")
    print()
    print("页面地址:")
    print("- PC管理页面: http://localhost:5000/manager ⭐")
    print("- 移动端页面: http://localhost:5000/mobile/{id}")
    print("- API文档: http://localhost:5000/api/config")
    print()
    print("配置信息:")
    print(f"- CSV目录: {CONFIG['CSV_DIR']}")
    print(f"- 图片目录: {CONFIG['IMAGE_DIR']}")
    print(f"- 公司API: {CONFIG['COMPANY_API_URL']}")
    print()
    print("="*70)
    print()
    print("💡 使用流程:")
    print("1. 电脑打开: http://localhost:5000/manager")
    print("2. 查看所有爆文和专属二维码")
    print("3. 手机扫描任意文章的二维码")
    print("4. 自动打开文章页面，点击发布")
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
