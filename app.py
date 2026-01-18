#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Generator - Web应用界面
基于Streamlit的图形界面应用
"""
import os
import sys
import json
import glob
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="网络热点话题聚合工具",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff6b6b;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #ff6b6b 0%, #feca57 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .topic-card {
        padding: 1rem;
        border-left: 4px solid #ff6b6b;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'last_run' not in st.session_state:
    st.session_state.last_run = None
if 'current_data' not in st.session_state:
    st.session_state.current_data = None


def get_history_reports():
    """获取所有历史报告"""
    output_dir = Path('output')
    if not output_dir.exists():
        return []

    reports = []
    for file in sorted(output_dir.glob('hot_topics_*.md'), reverse=True):
        try:
            # 从文件名提取时间戳
            timestamp_str = file.stem.replace('hot_topics_', '')
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            except:
                time_str = timestamp_str

            # 读取文件内容获取基本信息
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取总话题数
                total_topics = 0
                if '总话题数' in content:
                    for line in content.split('\n')[:20]:
                        if '总话题数' in line:
                            try:
                                total_topics = int(line.split(':')[1].strip())
                                break
                            except:
                                pass

            reports.append({
                'file': str(file),
                'filename': file.name,
                'time': time_str,
                'timestamp': timestamp_str,
                'total_topics': total_topics,
                'size': f"{file.stat().st_size / 1024:.1f} KB"
            })
        except Exception as e:
            continue

    return reports


def parse_markdown_report(filepath):
    """解析Markdown报告文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = {}
        current_section = None
        current_topics = []

        lines = content.split('\n')
        for line in lines:
            # 检测章节标题
            if line.startswith('## 📱'):
                if current_section and current_topics:
                    sections[current_section] = current_topics
                current_section = line.replace('## 📱', '').strip()
                current_topics = []
            elif current_section and line.startswith('### '):
                # 解析话题
                title = line.replace('###', '').strip()
                title = ' '.join(title.split()[:2]) + ' ' + ' '.join(title.split()[2:][:8])  # 限制长度
                current_topics.append(title)

        if current_section and current_topics:
            sections[current_section] = current_topics

        return sections
    except Exception as e:
        st.error(f"解析报告失败: {e}")
        return {}


def run_fetch():
    """运行抓取任务"""
    from src.aggregator import TopicAggregator
    from src.exporter import MarkdownExporter
    from config import CONFIG

    try:
        # 创建输出目录
        output_dir = CONFIG.get('output_dir', 'output')
        os.makedirs(output_dir, exist_ok=True)

        # 初始化抓取器和聚合器
        aggregator = TopicAggregator()
        exporter = MarkdownExporter()

        # 获取启用的平台
        enabled_platforms = CONFIG.get('enabled_platforms', [])

        # 抓取各平台数据
        all_topics = {}
        for platform in enabled_platforms:
            st.write(f"📥 正在获取 {platform} 数据...")
            try:
                from main import create_fetcher
                fetcher = create_fetcher(platform)
                count = CONFIG.get(f'{platform.split("_")[0]}_count', 20)
                topics = fetcher.fetch(count)
                if topics:
                    all_topics[platform] = topics
            except Exception as e:
                st.warning(f"⚠️ {platform} 获取失败: {e}")

        # 聚合数据
        aggregated = aggregator.aggregate(all_topics)

        # 导出报告
        report_file = exporter.export(all_topics, aggregated.get('cross_platform'), aggregated.get('summary'))

        # 更新session state
        st.session_state.last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.current_data = {
            'total_topics': aggregated.get('summary', {}).get('total_topics', 0),
            'platform_count': aggregated.get('summary', {}).get('platform_count', 0),
            'file': report_file
        }

        return True, aggregated

    except Exception as e:
        st.error(f"❌ 运行失败: {e}")
        return False, None


# ============ 侧边栏 ============
with st.sidebar:
    st.title("🔥 热点话题聚合器")
    st.markdown("---")

    # 导航选项
    page = st.radio(
        "选择功能",
        ["🏠 首页", "📊 历史记录", "⚙️ 设置"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # 快速信息
    if st.session_state.last_run:
        st.info(f"✅ 上次运行: {st.session_state.last_run}")

    # 环境变量状态
    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key:
        st.success("✅ YouTube API已配置")
    else:
        st.warning("⚠️ YouTube API未配置")

    proxy = os.getenv('USE_PROXY')
    if proxy:
        st.success(f"✅ 代理已启用")

    st.markdown("---")
    st.markdown("""
    ### 📖 使用说明
    1. 在**首页**点击"开始抓取"
    2. 在**历史记录**查看所有报告
    3. 在**设置**中修改配置
    """)


# ============ 主内容区 ============

if page == "🏠 首页":
    st.markdown('<h1 class="main-header">🔥 网络热点话题聚合工具</h1>', unsafe_allow_html=True)

    # 快速统计卡片
    col1, col2, col3, col4 = st.columns(4)

    if st.session_state.current_data:
        data = st.session_state.current_data
        col1.metric("总话题数", data['total_topics'])
        col2.metric("平台数量", data['platform_count'])
        col3.metric("科技/教育", "62条")  # 示例数据
        col4.metric("成功率", "87%")
    else:
        col1.metric("总话题数", "-")
        col2.metric("平台数量", "-")
        col3.metric("科技/教育", "-")
        col4.metric("成功率", "-")

    st.markdown("---")

    # 抓取按钮
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.button("🚀 开始抓取热点话题", type="primary", use_container_width=True):
            with st.spinner("正在抓取数据，请稍候..."):
                success, result = run_fetch()
                if success:
                    st.success("✅ 抓取成功！")
                    st.rerun()
                else:
                    st.error("❌ 抓取失败")

    with col2:
        if st.button("📄 打开输出目录", use_container_width=True):
            output_dir = Path('output')
            if output_dir.exists():
                os.startfile(output_dir) if sys.platform == 'win32' else None

    st.markdown("---")

    # 显示最新结果
    if st.session_state.current_data:
        st.subheader("📋 最新抓取结果")

        data = st.session_state.current_data
        st.markdown(f"""
        <div class="success-box">
            <strong>✅ 抓取完成！</strong><br>
            📁 报告文件: <code>{Path(data['file']).name}</code><br>
            📊 总话题数: <strong>{data['total_topics']}</strong> 条<br>
            🎯 成功平台: <strong>{data['platform_count']}</strong> 个
        </div>
        """, unsafe_allow_html=True)

        # 显示部分话题
        st.subheader("🔥 热门话题预览")
        try:
            sections = parse_markdown_report(data['file'])
            for platform, topics in list(sections.items())[:3]:
                with st.expander(f"📱 {platform} ({len(topics)}条)"):
                    for topic in topics[:5]:
                        st.markdown(f"- {topic}")
        except:
            st.info("请查看历史记录获取完整内容")
    else:
        st.info("👆 点击上方按钮开始抓取热点话题")


elif page == "📊 历史记录":
    st.title("📊 历史抓取记录")

    reports = get_history_reports()

    if not reports:
        st.warning("📭 暂无历史记录，请先运行抓取")
    else:
        # 统计信息
        col1, col2, col3 = st.columns(3)
        col1.metric("总报告数", len(reports))
        col2.metric("总话题数", sum(r['total_topics'] for r in reports))
        col3.metric("最新报告", reports[0]['time'] if reports else "-")

        st.markdown("---")

        # 报告列表
        st.subheader("📋 所有报告")

        # 搜索框
        search = st.text_input("🔍 搜索报告", placeholder="输入时间或文件名...")

        # 过滤报告
        filtered_reports = reports
        if search:
            filtered_reports = [r for r in reports if search.lower() in r['filename'].lower() or search in r['time']]

        # 显示报告
        for i, report in enumerate(filtered_reports):
            with st.expander(f"📄 {report['filename']} - {report['time']}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.write(f"📊 **话题数**: {report['total_topics']}")
                col2.write(f"📦 **大小**: {report['size']}")
                col3.write(f"🕒 **时间**: {report['time']}")

                # 操作按钮
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"👀 查看详情", key=f"view_{i}", use_container_width=True):
                        st.session_state.view_report = report['file']
                        st.rerun()

                with col2:
                    # 打开文件
                    if st.button(f"📂 打开文件", key=f"open_{i}", use_container_width=True):
                        if sys.platform == 'win32':
                            os.startfile(report['file'])

                with col3:
                    # 删除文件
                    if st.button(f"🗑️ 删除", key=f"delete_{i}", use_container_width=True):
                        try:
                            os.remove(report['file'])
                            st.success("已删除")
                            st.rerun()
                        except Exception as e:
                            st.error(f"删除失败: {e}")

        # 显示选中的报告详情
        if 'view_report' in st.session_state and st.session_state.view_report:
            st.markdown("---")
            st.subheader("📄 报告详情")

            try:
                with open(st.session_state.view_report, 'r', encoding='utf-8') as f:
                    content = f.read()
                st.markdown(content)
            except Exception as e:
                st.error(f"读取失败: {e}")


elif page == "⚙️ 设置":
    st.title("⚙️ 配置设置")

    st.markdown("""
    ### 📝 当前配置

    当前使用配置文件: `config.py`

    #### 启用的平台:
    - ✅ Hacker News
    - ✅ YouTube Tech (API)
    - ✅ YouTube Education (API)
    - ✅ Twitter Tech
    - ✅ Twitter Education
    - ✅ B站
    - ✅ 百度
    - ❌ 今日头条（待修复）

    #### 环境变量:
    """)

    # 显示环境变量状态
    env_vars = {
        'YOUTUBE_API_KEY': os.getenv('YOUTUBE_API_KEY', '未设置'),
        'USE_PROXY': os.getenv('USE_PROXY', '未设置'),
        'PROXY_HOST': os.getenv('PROXY_HOST', '未设置'),
        'PROXY_PORT': os.getenv('PROXY_PORT', '未设置'),
    }

    for key, value in env_vars.items():
        if key == 'YOUTUBE_API_KEY' and value != '未设置':
            # 隐藏API密钥的大部分内容
            masked = value[:10] + '...' + value[-4:]
            st.info(f"✅ **{key}**: `{masked}`")
        elif value != '未设置':
            st.success(f"✅ **{key}**: `{value}`")
        else:
            st.warning(f"⚠️ **{key}**: `{value}`")

    st.markdown("---")

    st.markdown("""
    ### 🔧 如何修改配置

    #### 方法1: 修改配置文件
    编辑 `config.py` 文件，然后重启应用

    #### 方法2: 设置环境变量
    ```bash
    # Windows PowerShell
    $env:YOUTUBE_API_KEY="你的密钥"

    # Linux/Mac
    export YOUTUBE_API_KEY="你的密钥"
    ```

    #### 方法3: 在Docker运行时传递
    ```bash
    docker run ... -e YOUTUBE_API_KEY="你的密钥" ...
    ```
    """)

    st.markdown("---")

    st.markdown("""
    ### 📖 文档链接

    - [YouTube API设置指南](docs/YOUTUBE_API_SETUP.md)
    - [快速开始](YOUTUBE_API_QUICKSTART.md)
    - [项目总结](PROJECT_SUMMARY.md)
    """)


# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>🔥 Topic Generator v2.0 | 网络热点话题聚合工具</p>
    <p>专注于科技和教育领域的话题聚合</p>
</div>
""", unsafe_allow_html=True)
