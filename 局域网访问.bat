@echo off
REM 热点抓取与爆文生成系统 - 局域网访问启动脚本
echo ================================================================================
echo 🚀 热点抓取与爆文生成系统 - 局域网访问模式
echo ================================================================================
echo.

REM 获取本机IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP: =!
    goto :found
)
:found

echo 📱 局域网访问地址
echo ================================================================================
echo.
echo ✅ 你的电脑可以访问:
echo    http://localhost:5000/
echo.
echo 🌐 同一WiFi的设备可以访问:
echo    http://!LOCAL_IP!:5000/
echo.
echo 💡 提示：
echo    - 确保你的防火墙允许Python访问网络
echo    - 确保设备连接到同一WiFi
echo    - 手机/平板浏览器直接访问上面的地址
echo.
echo ================================================================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python
    pause
    exit /b 1
)

REM 检查数据库
echo 📡 检查数据库连接...
python -c "from src.database.connection import test_connection; exit(0 if test_connection() else 1)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  数据库连接失败
    echo 💡 提示：首次运行请先执行: python scripts\init_db.py
    pause
    exit /b 1
)

echo ✅ 数据库连接正常
echo.

REM 启动Web服务器
echo 🌐 启动Web服务器...
echo    监听地址: 0.0.0.0:5000 (所有网卡)
echo.
echo 💡 提示：按 Ctrl+C 停止服务
echo ================================================================================
echo.

REM 启动服务器（监听所有网卡）
python run_web.py

pause
