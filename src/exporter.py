"""
Markdown导出器
"""
from typing import List, Dict
from datetime import datetime
from os import path
import sys

# 添加父目录到路径以导入config
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from config import CONFIG


class MarkdownExporter:
    """将热点话题导出为Markdown格式"""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or CONFIG.get('output_dir', 'output')

    def export(self, platform_topics: Dict[str, List[Dict]],
               cross_platform: List[tuple] = None,
               summary: Dict = None) -> str:
        """
        导出所有话题到Markdown文件

        Args:
            platform_topics: 按平台分组的话题
            cross_platform: 跨平台话题列表
            summary: 统计摘要

        Returns:
            导出文件的路径
        """
        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"hot_topics_{timestamp}.md"
        filepath = path.join(self.output_dir, filename)

        # 构建Markdown内容
        content = self._build_markdown(platform_topics, cross_platform, summary)

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Markdown报告已生成: {filepath}")
        return filepath

    def _build_markdown(self, platform_topics: Dict[str, List[Dict]],
                        cross_platform: List[tuple] = None,
                        summary: Dict = None) -> str:
        """构建Markdown内容"""

        lines = []
        lines.append("# 🔥 网络热点话题聚合报告\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 添加摘要统计
        if summary:
            lines.append("## 📊 数据概览\n")
            lines.append(f"- **总话题数**: {summary.get('total_topics', 0)}")
            lines.append(f"- **平台数量**: {summary.get('platform_count', 0)}")
            lines.append(f"- **跨平台热点**: {summary.get('cross_platform_count', 0)}")
            lines.append("")

        # 添加跨平台热点
        if cross_platform and len(cross_platform) > 0:
            lines.append("## 🔗 跨平台热点\n")
            lines.append("以下话题在多个平台同时出现：\n")
            for title, platforms in cross_platform[:10]:
                badges = ' '.join([f"`{p}`" for p in platforms])
                lines.append(f"- {title} {badges}")
            lines.append("")

        # 添加各平台热点
        for platform, topics in platform_topics.items():
            lines.append(f"## 📱 {platform}\n")

            for topic in topics[:20]:  # 每个平台最多显示20条
                rank = topic.get('rank', 0)
                title = topic.get('title', '')
                url = topic.get('url', '')
                hot_value = topic.get('hot_value', 0)

                # 确保hot_value是数字类型
                try:
                    hot_value = int(hot_value)
                except (ValueError, TypeError):
                    hot_value = 0

                # 格式化热度值
                if hot_value > 100000000:
                    hot_str = f"{hot_value/100000000:.1f}亿"
                elif hot_value > 10000:
                    hot_str = f"{hot_value/10000:.1f}万"
                else:
                    hot_str = str(hot_value)

                lines.append(f"### {rank}. {title}")
                if url:
                    lines.append(f"- **链接**: [{url}]({url})")
                if hot_value:
                    lines.append(f"- **热度**: {hot_str}")
                lines.append("")

        # 添加页脚
        lines.append("---\n")
        lines.append("*本报告由 Topic Generator 自动生成*")

        return '\n'.join(lines)
