@echo off
chcp 65001 >nul
title Topic Generator - With YouTube API

echo ========================================
echo 🔥 Topic Generator - 全平台抓取
echo ========================================
echo.
echo ✅ YouTube API: 已启用
echo ✅ 平台: Hacker News + YouTube + Twitter + 今日头条 + B站
echo.
echo 开始抓取...
echo.

REM 设置YouTube API密钥
set YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk

REM 运行主程序
python main.py

echo.
echo ========================================
echo 抓取完成！现在生成小红书爆文...
echo ========================================
echo.

python xiaohongshu_generator.py

echo.
echo ========================================
echo ✅ 全部完成！
echo ========================================
echo.
echo 输出文件位置:
echo - 热点话题: output\hot_topics_*.md
echo - 小红书爆文: output\xiaohongshu_posts_*.csv
echo - H5发布页面: h5\xiaohongshu_publish.html
echo.
pause
