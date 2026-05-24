# 🎬 BiliLite - 轻量级视频分享平台

一个基于 FastAPI + Vue 3 的全栈视频分享网站，个人开发学习项目，模仿 B 站核心功能。

> **声明**: 此网站仅仅是个人开发学习和测试上线使用，不会用于商业用途，尊重原作者，尊重 B 站。

---

## 📸 功能概览

| 功能 | 说明 |
|------|------|
| 📹 **视频上传** | 用户自助上传，需填写标题、标签、封面 |
| 🏠 **首页推荐** | 按播放量排序，支持标签分类筛选（游戏/舞蹈/生活等） |
| 🏆 **排行榜** | 综合/点赞数/收藏数 三种排序 |
| 🔍 **视频搜索** | 按标题和 UP 主名搜索 |
| 👤 **用户系统** | 注册、登录、个人中心 |
| ❤️ **互动系统** | 点赞、收藏、关注、评论（含回复）、投币 |
| ⏱️ **播放统计** | 实时记录观看数、点赞数、收藏数 |

---

## 🛠️ 技术栈

### 后端
| 技术 | 用途 |
|------|------|
| Python 3.11+ | 运行时 |
| FastAPI | Web 框架 |
| SQLAlchemy 2.0 (async) | ORM |
| SQLite (开发) / MySQL (生产) | 数据库 |
| JWT + bcrypt | 用户认证 |
| python-multipart | 文件上传 |

### 前端
| 技术 | 用途 |
|------|------|
| Vue 3 (Composition API) | UI 框架 |
| TypeScript | 类型安全 |
| Vite 4.5 | 构建工具 |
| Pinia | 状态管理 |
| Tailwind CSS | 样式 |
| Element Plus 2.x | UI 组件库 |
| Axios | HTTP 请求 |

---

## 🚀 快速开始

### 前置要求
- Python 3.11+
- Node.js 18+
- npm 9+

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/bililite.git
cd bililite
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

后端运行在 `http://localhost:8000`

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`

### 4. 开始使用

1. 打开浏览器访问 `http://localhost:5173`
2. 注册账号 → 登录
3. 点击右上角「投稿」上传视频（需填写标题、标签、封面）
4. 上传完成后视频自动出现在首页

---

## 📁 项目结构

```
bililite/
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── video.py    # 视频/上传/点赞/收藏
│   │   │   ├── user.py     # 用户/关注/头像
│   │   │   ├── auth.py     # 登录/注册
│   │   │   ├── comment.py  # 评论/回复/评论点赞
│   │   │   └── danmaku.py  # 弹幕（已弃用）
│   │   ├── models/         # SQLAlchemy 模型
│   │   ├── schemas/        # Pydantic 数据模式
│   │   └── core/           # 配置/安全/数据库
│   ├── uploads/            # 用户上传的文件
│   │   ├── videos/         # 视频文件
│   │   ├── covers/         # 封面图片
│   │   └── avatars/        # 用户头像
│   └── requirements.txt    # Python 依赖
│
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面
│   │   ├── components/     # 组件
│   │   ├── stores/         # Pinia 状态
│   │   ├── api/            # API 封装
│   │   ├── router/         # 路由
│   │   └── utils/          # 工具函数
│   └── package.json        # NPM 依赖
│
└── README.md
```

---

## 📡 API 文档

启动后端后访问 `http://localhost:8000/docs` 查看交互式 API 文档。

### 主要接口

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| `GET` | `/api/video/home` | 首页推荐（可选 `?tag=` 筛选） | ❌ |
| `GET` | `/api/video/ranking` | 排行榜（可选 `?sort=hot/like/collect`） | ❌ |
| `GET` | `/api/video/search?q=` | 搜索视频 | ❌ |
| `GET` | `/api/video/detail/{bvid}` | 视频详情（自动 +1 播放量） | ❌ |
| `POST` | `/api/video/upload` | 上传视频 | ✅ |
| `POST` | `/api/video/{id}/like` | 点赞/取消点赞 | ✅ |
| `POST` | `/api/video/{id}/collect` | 收藏/取消收藏 | ✅ |
| `GET` | `/api/video/likes` | 我的点赞列表 | ✅ |
| `GET` | `/api/video/collections` | 我的收藏列表 | ✅ |
| `POST` | `/api/auth/register` | 注册 | ❌ |
| `POST` | `/api/auth/login` | 登录 | ❌ |
| `GET` | `/api/user/profile` | 个人信息 | ✅ |
| `POST` | `/api/user/follow/{id}` | 关注/取消关注 | ✅ |
| `GET` | `/api/user/follows` | 我的关注列表 | ✅ |
| `POST` | `/api/user/avatar` | 上传头像 | ✅ |
| `GET` | `/api/comment/video/{id}` | 视频评论（含回复） | ❌ |
| `POST` | `/api/comment` | 发表评论/回复 | ✅ |
| `POST` | `/api/comment/{id}/like` | 评论点赞/取消 | ✅ |

---

## 🗄️ 数据存储

### 数据库
- 默认使用 **SQLite**（`backend/test.db`），无需额外安装数据库
- 生产环境可切换 **MySQL**，修改 `backend/.env` 配置即可

### 文件存储
```
backend/uploads/
├── videos/    ← 上传的视频文件 (.mp4/.webm/.mov)
├── covers/    ← 上传的封面图片 (.jpg/.png/.webp)
└── avatars/   ← 用户头像
```

这些文件与数据库一同构成完整数据，迁移时需一并复制。

---

## 🌐 生产部署

### Docker 部署（推荐）

```dockerfile
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend/uploads:/app/uploads   # 文件持久化
      - ./backend/test.db:/app/test.db   # 数据库持久化
```

### 直接部署

```bash
# 前端构建
cd frontend
npm run build   # 输出到 dist/

# 然后用 Nginx 托管前端静态文件 + 反向代理 /api 到后端
```

> **注意**: 每次迁移需保证 `test.db`（数据库）和 `uploads/`（文件）一并转移。

---

## 🔧 常见问题

**Q: 上传视频提示格式不支持？**
A: 支持 mp4、webm、mov、avi、mkv 格式。封面需 jpg/png/webp。

**Q: 上传后视频无法播放？**
A: 检查文件是否成功上传到 `backend/uploads/videos/`，以及浏览器是否支持该视频编码（推荐 H.264）。

**Q: 如何修改标签列表？**
A: 前端修改 `frontend/src/views/UploadPage.vue` 中的 `ALLOWED_TAGS` 数组；后端直接改即可。

**Q: 数据库和文件如何备份？**
A: 复制 `backend/test.db` 和整个 `backend/uploads/` 目录即可。

---

## 📄 许可证

MIT License

```
Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

**Made for learning purposes — 个人学习开发，尊重原创内容**
