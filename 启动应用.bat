@echo off
chcp 65001 >nul
title Topic Generator - 网络热点话题聚合工具

echo ========================================
echo 🔥 Topic Generator 启动中...
echo ========================================
echo.

REM 检查Docker是否运行
docker ps >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未运行，请先启动Docker Desktop
    echo.
    pause
    exit /b 1
)

echo ✅ Docker已就绪
echo.
echo 🚀 正在启动Web应用...
echo.
echo 应用将在浏览器中自动打开
echo 按 Ctrl+C 可以停止应用
echo.
echo ========================================
echo.

REM 启动Streamlit应用
docker run --rm ^
    -e USE_PROXY=true ^
    -e PROXY_HOST=host.docker.internal ^
    -e PROXY_PORT=10810 ^
    -e YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk ^
    -p 8501:8501 ^
    -v "%~dp0:/app" ^
    -w /app ^
    python:3.8-slim ^
    bash -c "pip install streamlit pandas requests python-dateutil beautifulsoup4 -q && streamlit run app.py --server.port=8501 --server.address=0.0.0.0"

pause
