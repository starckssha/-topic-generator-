@echo off
chcp 65001 >nul
title 小红书爆文发布系统 - 一键启动

echo ========================================
echo 🔥 小红书爆文发布系统 - 一键启动
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境检测通过
echo.

REM 检查依赖
echo [*] 检查依赖包...
python -c "import flask, flask_cors, pandas, qrcode, PIL" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少依赖包，正在安装...
    pip install flask flask-cors pandas qrcode pillow
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖包检测通过
echo.

REM 检查CSV文件
echo [*] 检查爆文数据...
if not exist "output\xiaohongshu_posts_*.csv" (
    echo ⚠️  未找到爆文数据，正在生成...
    python convert_to_csv.py
)

echo ✅ 数据文件就绪
echo.

REM 生成二维码
echo [*] 生成二维码...
python generate_qrcode.py
echo.

echo ========================================
echo 🚀 准备启动后端服务...
echo ========================================
echo.
echo 服务地址: http://localhost:5000
echo H5页面: http://localhost:5000/h5/index.html
echo.
echo 💡 提示:
echo - 按 Ctrl+C 停止服务
echo - 手机扫描二维码访问H5页面
echo - 二维码位置: output/xiaohongshu_qrcode_medium.png
echo.
echo ========================================
echo.

REM 启动Flask服务
python app_flask.py

pause
