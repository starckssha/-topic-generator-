@echo off
chcp 65001 >nul
echo ======================================================================
echo Google Nano Banana (Gemini) 图片生成 - 快速配置
echo ======================================================================
echo.

echo 📝 请输入你的 Google API Key
echo ------------------------------------
echo 💡 获取 API Key:
echo    1. 访问 https://aistudio.google.com/app/apikey
echo    2. 登录 Google 账号
echo    3. 点击 "Create API Key"
echo    4. 复制 API Key（格式：AIzaSy...）
echo.
echo ------------------------------------

set /p API_KEY="请输入 API Key: "

if "%API_KEY%"=="" (
    echo ❌ API Key 不能为空！
    pause
    exit /b 1
)

echo.
echo 🔧 正在配置环境变量...

setx GOOGLE_API_KEY "%API_KEY%" >nul 2>&1
set GOOGLE_API_KEY=%API_KEY%

echo.
echo ✅ 配置完成！
echo.
echo ======================================================================
echo 🧪 测试图片生成...
echo ======================================================================
echo.

python nano_banana_generator.py

echo.
echo ======================================================================
echo 🎉 配置成功！
echo ======================================================================
echo.
echo 💡 接下来:
echo    1. 重启 Flask 服务: python app_flask.py
echo    2. 刷新移动端页面，查看生成的配图
echo    3. 检查图片URL中包含 'nano_banana' 即为成功
echo.
pause
