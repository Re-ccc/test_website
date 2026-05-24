from fastapi import APIRouter, Depends, HTTPException, Query, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.video import Video as VideoModel
from app.models.like import Like as LikeModel
from app.models.collection import Collection as CollectionModel
from app.models.user import User as UserModel
from app.schemas.video import Video, VideoLikeResponse, VideoCollectResponse
import uuid
import os
import math
import struct

router = APIRouter()

UPLOAD_DIR = "uploads"
VIDEO_DIR = os.path.join(UPLOAD_DIR, "videos")
COVER_DIR = os.path.join(UPLOAD_DIR, "covers")


def get_video_duration(filepath: str) -> int:
    """解析 MP4/MOV 文件头获取时长（秒），无需外部依赖"""
    try:
        with open(filepath, "rb") as f:
            data = f.read(256 * 1024)
        offset = 0
        while offset < len(data) - 8:
            size = struct.unpack(">I", data[offset:offset + 4])[0]
            if size < 8:
                break
            box_type = data[offset + 4:offset + 8].decode("latin-1", errors="replace")
            if box_type == "moov":
                inner = data[offset + 8:offset + size]
                ioff = 0
                while ioff < len(inner) - 8:
                    isize = struct.unpack(">I", inner[ioff:ioff + 4])[0]
                    if isize < 8:
                        break
                    itype = inner[ioff + 4:ioff + 8].decode("latin-1", errors="replace")
                    if itype == "mvhd":
                        ver = inner[ioff + 8]
                        if ver == 0:
                            timescale = struct.unpack(">I", inner[ioff + 20:ioff + 24])[0]
                            duration = struct.unpack(">I", inner[ioff + 24:ioff + 28])[0]
                        else:
                            timescale = struct.unpack(">I", inner[ioff + 28:ioff + 32])[0]
                            duration = struct.unpack(">Q", inner[ioff + 32:ioff + 40])[0]
                        return int(duration / timescale) if timescale > 0 else 0
                    ioff += isize
                break
            offset += size
    except Exception:
        pass
    return 0


def generate_bvid() -> str:
    """生成唯一的 BV 号"""
    raw = uuid.uuid4().hex[:12]
    return f"BV{raw.upper()}"


@router.get("/home", response_model=List[Video])
async def get_home_feed(
    tag: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """首页推荐 - 按播放量排序，支持标签筛选"""
    query = select(VideoModel).order_by(desc(VideoModel.view_count)).limit(20)
    if tag:
        query = query.where(VideoModel.tags.like(f"%{tag}%"))
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/ranking", response_model=List[Video])
async def get_ranking(
    sort: str = Query("hot"),
    db: AsyncSession = Depends(get_db),
):
    """热门排行榜 - hot(综合)/like(点赞)/collect(收藏)"""
    if sort == "like":
        order_col = VideoModel.like_count
    elif sort == "collect":
        order_col = VideoModel.collect_count
    else:
        order_col = VideoModel.view_count * 0.6 + VideoModel.like_count * 0.4 + VideoModel.collect_count * 0.3
    result = await db.execute(
        select(VideoModel).order_by(desc(order_col)).limit(30)
    )
    return list(result.scalars().all())


@router.get("/search", response_model=List[Video])
async def search_videos(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    """搜索视频 - 按标题和UP主名关键字匹配"""
    keyword = f"%{q}%"
    result = await db.execute(
        select(VideoModel).where(
            or_(
                VideoModel.title.like(keyword),
                VideoModel.uploader_name.like(keyword)
            )
        ).order_by(desc(VideoModel.view_count))
    )
    return list(result.scalars().all())


@router.get("/detail/{bvid}", response_model=Video)
async def get_video_detail(bvid: str, db: AsyncSession = Depends(get_db)):
    """获取视频详情"""
    result = await db.execute(select(VideoModel).where(VideoModel.bvid == bvid))
    video = result.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    video.view_count += 1
    await db.commit()
    await db.refresh(video)
    return video


@router.get("/{video_id}/related", response_model=List[Video])
async def get_related_videos(video_id: int, db: AsyncSession = Depends(get_db)):
    """获取相关视频推荐"""
    result = await db.execute(select(VideoModel).where(VideoModel.id == video_id))
    current = result.scalars().first()
    if current:
        keyword = current.title[:4]
        result = await db.execute(
            select(VideoModel).where(
                and_(
                    VideoModel.id != video_id,
                    VideoModel.title.like(f"%{keyword}%")
                )
            ).order_by(desc(VideoModel.view_count)).limit(10)
        )
        videos = result.scalars().all()
        if len(videos) >= 3:
            return list(videos)
    result = await db.execute(
        select(VideoModel).where(VideoModel.id != video_id)
        .order_by(desc(VideoModel.view_count)).limit(10)
    )
    return list(result.scalars().all())


@router.post("/upload", response_model=Video)
async def upload_video(
    video_file: UploadFile = File(...),
    cover_file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """上传视频 - 需要登录，封面和标签必填"""
    if not title.strip():
        raise HTTPException(status_code=400, detail="标题不能为空")
    if not tags.strip():
        raise HTTPException(status_code=400, detail="至少需要添加一个标签")

    # 校验封面文件类型
    cover_ext = cover_file.filename.rsplit(".", 1)[-1].lower() if "." in (cover_file.filename or "") else ""
    if cover_ext not in ("jpg", "jpeg", "png", "webp"):
        raise HTTPException(status_code=400, detail="封面必须是 jpg/png/webp 格式")

    # 校验视频文件类型
    video_ext = video_file.filename.rsplit(".", 1)[-1].lower() if "." in (video_file.filename or "") else ""
    if video_ext not in ("mp4", "webm", "mov", "avi", "mkv"):
        raise HTTPException(status_code=400, detail="视频格式不支持，请上传 mp4/webm/mov 格式")

    bvid = generate_bvid()

    # 保存视频
    video_filename = f"{bvid}.{video_ext}"
    video_path = os.path.join(VIDEO_DIR, video_filename)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    with open(video_path, "wb") as f:
        content = await video_file.read()
        f.write(content)

    # 保存封面
    cover_filename = f"{bvid}.{cover_ext}"
    cover_path = os.path.join(COVER_DIR, cover_filename)
    os.makedirs(COVER_DIR, exist_ok=True)
    with open(cover_path, "wb") as f:
        content = await cover_file.read()
        f.write(content)

    duration = get_video_duration(video_path)

    video_record = VideoModel(
        bvid=bvid,
        title=title.strip(),
        description=description.strip(),
        cover_url=f"/uploads/covers/{cover_filename}",
        video_url=f"/uploads/videos/{video_filename}",
        duration=duration,
        tags=tags.strip(),
        uploader_id=current_user.id,
        uploader_name=current_user.nickname or current_user.username,
        uploader_avatar=current_user.avatar_url or "",
    )
    db.add(video_record)
    await db.commit()
    await db.refresh(video_record)
    return video_record


@router.post("/{video_id}/like", response_model=VideoLikeResponse)
async def like_video(
    video_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """点赞/取消点赞"""
    result = await db.execute(
        select(LikeModel).where(
            and_(LikeModel.user_id == current_user.id, LikeModel.video_id == video_id)
        )
    )
    like = result.scalars().first()
    result = await db.execute(select(VideoModel).where(VideoModel.id == video_id))
    video = result.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    if like:
        await db.delete(like)
        video.like_count = max(0, video.like_count - 1)
        await db.commit()
        return {"success": True, "liked": False, "like_count": video.like_count}
    new_like = LikeModel(user_id=current_user.id, video_id=video_id)
    db.add(new_like)
    video.like_count += 1
    await db.commit()
    return {"success": True, "liked": True, "like_count": video.like_count}


@router.post("/{video_id}/collect", response_model=VideoCollectResponse)
async def collect_video(
    video_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """收藏/取消收藏"""
    result = await db.execute(
        select(CollectionModel).where(
            and_(CollectionModel.user_id == current_user.id, CollectionModel.video_id == video_id)
        )
    )
    collect = result.scalars().first()
    result = await db.execute(select(VideoModel).where(VideoModel.id == video_id))
    video = result.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    if collect:
        await db.delete(collect)
        video.collect_count = max(0, video.collect_count - 1)
        await db.commit()
        return {"success": True, "collected": False, "collect_count": video.collect_count}
    new_collect = CollectionModel(user_id=current_user.id, video_id=video_id)
    db.add(new_collect)
    video.collect_count += 1
    await db.commit()
    return {"success": True, "collected": True, "collect_count": video.collect_count}


@router.get("/collections", response_model=List[Video])
async def get_my_collections(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """我的收藏"""
    result = await db.execute(
        select(VideoModel)
        .join(CollectionModel, CollectionModel.video_id == VideoModel.id)
        .where(CollectionModel.user_id == current_user.id)
        .order_by(desc(CollectionModel.created_at))
    )
    return list(result.scalars().all())


@router.get("/likes", response_model=List[Video])
async def get_my_likes(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """我的点赞"""
    result = await db.execute(
        select(VideoModel)
        .join(LikeModel, LikeModel.video_id == VideoModel.id)
        .where(LikeModel.user_id == current_user.id)
        .order_by(desc(LikeModel.created_at))
    )
    return list(result.scalars().all())
