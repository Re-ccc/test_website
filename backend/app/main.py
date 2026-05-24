from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import video, auth, danmaku, comment, user
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.collection import Collection
from app.models.comment_like import CommentLike
import os

app = FastAPI(title="Bilibili Clone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(danmaku.router, prefix="/api/danmaku", tags=["danmaku"])
app.include_router(comment.router, prefix="/api/comment", tags=["comment"])
app.include_router(user.router, prefix="/api/user", tags=["user"])

os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/covers", exist_ok=True)
os.makedirs("uploads/avatars", exist_ok=True)
os.makedirs("data", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Bilibili Clone API"}
