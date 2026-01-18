@echo off
REM 热点抓取与爆文生成系统 - 启动脚本
echo ================================================================================
echo 🚀 热点抓取与爆文生成系统
echo ================================================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境检测通过
echo.

REM 检查数据库连接
echo 📡 检查数据库连接...
python -c "from src.database.connection import test_connection; exit(0 if test_connection() else 1)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  数据库连接失败，请检查网络或配置
    echo 💡 提示：首次运行请先执行: python scripts\init_db.py
    pause
    exit /b 1
)

echo ✅ 数据库连接正常
echo.

REM 启动Web服务器
echo 🌐 启动Web服务器...
echo 📊 访问地址: http://localhost:5000
echo 📱 管理页面: http://localhost:5000/manager
echo.
echo 💡 提示：按 Ctrl+C 停止服务
echo ================================================================================
echo.

python run_web.py

pause
