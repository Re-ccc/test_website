@echo off
echo ========================================
echo   B站模仿项目 - MySQL数据库初始化
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 正在安装Python依赖...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [2/4] 正在创建数据库...
python scripts\init_database.py
if errorlevel 1 (
    echo [错误] 数据库创建失败
    pause
    exit /b 1
)

echo.
echo [3/4] 正在创建数据表...
python scripts\create_tables.py
if errorlevel 1 (
    echo [错误] 数据表创建失败
    pause
    exit /b 1
)

echo.
echo [4/4] 正在启动服务器...
echo.
echo ========================================
echo   启动成功！
echo   后端服务: http://localhost:8000
echo   API文档:  http://localhost:8000/docs
echo ========================================
echo.
echo 按 Ctrl+C 停止服务器
echo.

python -m uvicorn app.main:app --reload --port 8000
