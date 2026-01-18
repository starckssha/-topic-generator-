@echo off
chcp 65001 >nul
title Topic Generator - 网络热点话题聚合工具

echo ========================================
echo 🔥 Topic Generator 启动中...
echo ========================================
echo.

REM 设置环境变量
set YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk

echo ✅ 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo.
    pause
    exit /b 1
)

echo ✅ Python已就绪
echo.
echo 🚀 正在安装/更新依赖包...
echo.

REM 安装依赖
pip install streamlit pandas requests python-dateutil beautifulsoup4 -q

echo.
echo ✅ 依赖包安装完成
echo.
echo 🚀 正在启动Web应用...
echo.
echo 应用将在浏览器中自动打开
echo 按 Ctrl+C 可以停止应用
echo.
echo ========================================
echo.

REM 启动Streamlit应用
streamlit run app.py

pause
