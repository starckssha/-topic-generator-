@echo off
chcp 65001 >nul
title Topic Generator 启动

echo ========================================
echo 🔥 Topic Generator 启动工具
echo ========================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

echo 当前目录: %CD%
echo.

REM 检查Python
echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python
    echo.
    echo 请安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python已安装
python --version
echo.

REM 安装依赖
echo [2/3] 安装依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.
pip install streamlit pandas requests python-dateutil beautifulsoup4 -q
if errorlevel 1 (
    echo ⚠️ 依赖安装可能有问题，但继续尝试...
)
echo ✅ 依赖包已就绪
echo.

REM 设置环境变量
echo [3/3] 启动应用...
echo.
set YOUTUBE_API_KEY=AIzaSyC8tCzhNoIYyUq8q9muz3Dqe3VR0A41wvk

echo ========================================
echo 🚀 正在启动Web应用...
echo ========================================
echo.
echo 应用将在浏览器中打开
echo 如果浏览器没有自动打开，请访问:
echo   http://localhost:8501
echo.
echo 按 Ctrl+C 可以停止应用
echo.
echo ========================================
echo.

REM 启动Streamlit
streamlit run app.py

echo.
echo ========================================
echo 应用已关闭
echo ========================================
pause
