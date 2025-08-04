@echo off
chcp 65001 >nul
echo 法学研究科研绘图工具
echo ====================
echo.
echo 正在启动程序...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖包是否安装
echo 检查依赖包...
pip show matplotlib >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
)

REM 运行程序
echo 启动绘图工具...
python main.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
) 