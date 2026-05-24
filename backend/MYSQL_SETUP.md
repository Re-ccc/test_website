# MySQL 数据库配置指南

## 前提条件

确保你已经安装了 MySQL 数据库（推荐 MySQL 8.0+）

## 配置步骤

### 1. 修改配置文件

打开 `backend\.env` 文件，修改以下配置：

```env
DB_HOST=localhost           # MySQL 服务器地址
DB_PORT=3306               # MySQL 端口（默认3306）
DB_USER=root               # MySQL 用户名
DB_PASSWORD=your_password  # 你的MySQL密码
DB_NAME=bilibili_clone     # 数据库名称
```

### 2. 创建数据库和表

#### Windows 用户
双击运行 `backend\start_with_mysql.bat`

#### Mac/Linux 用户
```bash
cd backend
chmod +x start_with_mysql.sh
./start_with_mysql.sh
```

#### 或手动执行
```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 创建数据库
python scripts/init_database.py

# 创建表
python scripts/create_tables.py

# 启动服务
python -m uvicorn app.main:app --reload --port 8000
```

## 数据库表结构

项目包含以下数据表：

| 表名 | 说明 |
|------|------|
| users | 用户信息表 |
| videos | 视频信息表 |
| danmakus | 弹幕表 |
| comments | 评论表 |
| likes | 点赞表 |
| follows | 关注表 |

## 注意事项

1. **字符集**：数据库使用 `utf8mb4` 字符集，支持完整的 Unicode 字符
2. **连接池**：已配置异步连接池，提高并发性能
3. **索引优化**：所有外键和常用查询字段都建立了索引

## 常见问题

### Q: 连接数据库失败？
A: 检查以下几点：
- MySQL 服务是否已启动
- 端口号是否正确
- 用户名密码是否正确
- 是否有远程连接权限

### Q: 如何重置数据库？
A: 删除数据库后重新运行初始化脚本：
```sql
DROP DATABASE IF EXISTS bilibili_clone;
```
然后重新运行 `start_with_mysql.bat`

### Q: 如何查看数据库内容？
A: 使用 MySQL 客户端工具（如 MySQL Workbench、Navicat）或命令行：
```bash
mysql -u root -p bilibili_clone
```
