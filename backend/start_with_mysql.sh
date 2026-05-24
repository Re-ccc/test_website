#!/bin/bash

echo "========================================"
echo "  B站模仿项目 - MySQL数据库初始化"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/4] 正在安装Python依赖..."
pip install -r requirements.txt

echo ""
echo "[2/4] 正在创建数据库..."
python scripts/init_database.py

echo ""
echo "[3/4] 正在创建数据表..."
python scripts/create_tables.py

echo ""
echo "[4/4] 正在启动服务器..."
echo ""
echo "========================================"
echo "  启动成功！"
echo "  后端服务: http://localhost:8000"
echo "  API文档:  http://localhost:8000/docs"
echo "========================================"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python -m uvicorn app.main:app --reload --port 8000
