@echo off
chcp 65001 >nul
echo ========================================
echo 法学研究科研绘图工具 - Web版本
echo ========================================
echo.

:: 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到Node.js
    echo 请先安装Node.js (https://nodejs.org/)
    echo 建议版本: 16.0.0 或更高
    pause
    exit /b 1
)

:: 检查npm是否安装
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到npm
    echo 请先安装npm
    pause
    exit /b 1
)

echo ✅ Node.js版本:
node --version
echo ✅ npm版本:
npm --version
echo.

:: 检查是否已安装依赖
if not exist "node_modules" (
    echo 📦 正在安装依赖包...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
)

:: 启动开发服务器
echo 🚀 启动开发服务器...
echo 📱 应用将在浏览器中自动打开
echo 🔗 本地地址: http://localhost:3000
echo.
echo 按 Ctrl+C 停止服务器
echo.

npm run dev

pause 