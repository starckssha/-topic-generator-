@echo off
chcp 65001 >nul
title Topic Generator 诊断工具

echo ========================================
echo 🔍 Topic Generator 环境诊断工具
echo ========================================
echo.

cd /d "%~dp0"

REM 检查Python
echo [检查 1/5] Python环境
echo ----------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 状态: 未安装Python
    echo.
    echo 解决方案:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.8 或更高版本
    echo 3. 安装时勾选 "Add Python to PATH"
    echo.
    set PYTHON_OK=0
) else (
    echo ✅ 状态: Python已安装
    python --version
    echo.
    set PYTHON_OK=1
)
pause
echo.

REM 检查pip
echo [检查 2/5] pip包管理器
echo ----------------------------------------
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 状态: pip未安装
    echo.
    set PIP_OK=0
) else (
    echo ✅ 状态: pip已安装
    pip --version
    echo.
    set PIP_OK=1
)
pause
echo.

REM 检查依赖包
echo [检查 3/5] 依赖包
echo ----------------------------------------
if %PYTHON_OK%==1 (
    for %%p in (streamlit pandas requests beautifulsoup4) do (
        echo 检查 %%p...
        pip show %%p >nul 2>&1
        if errorlevel 1 (
            echo ❌ %%p 未安装
        ) else (
            echo ✅ %%p 已安装
        )
    )
) else (
    echo ⏭️  跳过（Python未安装）
)
echo.
pause
echo.

REM 检查文件
echo [检查 4/5] 项目文件
echo ----------------------------------------
if exist "app.py" (
    echo ✅ app.py 存在
) else (
    echo ❌ app.py 不存在
)

if exist "config.py" (
    echo ✅ config.py 存在
) else (
    echo ❌ config.py 不存在
)

if exist "src\fetchers\__init__.py" (
    echo ✅ src 模块存在
) else (
    echo ❌ src 模块不完整
)
echo.
pause
echo.

REM 检查端口
echo [检查 5/5] 端口占用
echo ----------------------------------------
netstat -ano | findstr ":8501" >nul 2>&1
if errorlevel 1 (
    echo ✅ 端口8501未被占用
} else (
    echo ⚠️  端口8501已被占用
    echo.
    echo 占用进程:
    netstat -ano | findstr ":8501"
    echo.
    echo 可能是之前的Streamlit实例还在运行
    echo 可以在任务管理器中结束 python.exe 进程
}
echo.
pause
echo.

REM 总结
echo ========================================
echo 📋 诊断总结
echo ========================================
echo.

if %PYTHON_OK%==0 (
    echo ❌ 主要问题: Python未安装
    echo.
    echo 请先安装Python，然后重新运行此诊断工具
    echo 下载: https://www.python.org/downloads/
) else (
    echo ✅ Python环境正常
    echo.
    echo 📝 下一步:
    echo 1. 如果缺少依赖包，运行: pip install streamlit pandas requests beautifulsoup4
    echo 2. 然后双击运行: 启动应用_简化版.bat
)

echo.
echo ========================================
echo.
pause

REM 如果环境正常，提供直接启动选项
if %PYTHON_OK%==1 (
    cls
    echo ========================================
    echo 环境检查完成，是否现在启动应用？
    echo ========================================
    echo.
    set /p START="输入 Y 启动应用，或其他键退出: "
    if /i "%START%"=="Y" (
        echo.
        echo 正在启动...
        start streamlit run app.py
    )
)
