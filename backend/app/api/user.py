from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User as UserModel
from app.models.follow import Follow as FollowModel
from app.models.video import Video as VideoModel
from app.schemas.user import User, UserUpdate
from app.schemas.video import Video
import uuid
import os

router = APIRouter()


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """上传头像"""
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else "png"
    if ext not in ("jpg", "jpeg", "png", "webp"):
        raise HTTPException(status_code=400, detail="头像必须是 jpg/png/webp 格式")

    filename = f"{uuid.uuid4().hex}.{ext}"
    avatar_dir = "uploads/avatars"
    os.makedirs(avatar_dir, exist_ok=True)
    filepath = os.path.join(avatar_dir, filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    avatar_url = f"/uploads/avatars/{filename}"
    result = await db.execute(select(UserModel).filter(UserModel.id == current_user.id))
    user = result.scalars().first()
    if user:
        user.avatar_url = avatar_url
        await db.commit()
        await db.refresh(user)
    return {"avatar_url": avatar_url}


@router.get("/profile", response_model=User)
async def get_profile(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserModel).filter(UserModel.id == current_user.id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/profile", response_model=User)
async def update_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserModel).filter(UserModel.id == current_user.id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user_update.nickname:
        user.nickname = user_update.nickname
    if user_update.avatar_url:
        user.avatar_url = user_update.avatar_url
    if user_update.signature:
        user.signature = user_update.signature
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/follow/{user_id}")
async def follow_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能关注自己")

    result = await db.execute(
        select(FollowModel).where(
            and_(
                FollowModel.follower_id == current_user.id,
                FollowModel.following_id == user_id,
            )
        )
    )
    follow = result.scalars().first()

    # 获取目标用户
    target_result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    target = target_result.scalars().first()
    if not target:
        raise HTTPException(status_code=404, detail="用户不存在")

    if follow:
        await db.delete(follow)
        current_user.following_count = max(0, current_user.following_count - 1)
        target.follower_count = max(0, target.follower_count - 1)
        await db.commit()
        return {"success": True, "followed": False}

    new_follow = FollowModel(follower_id=current_user.id, following_id=user_id)
    db.add(new_follow)
    current_user.following_count += 1
    target.follower_count += 1
    await db.commit()
    return {"success": True, "followed": True}


@router.get("/follows", response_model=List[User])
async def get_my_follows(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """我的关注"""
    result = await db.execute(
        select(UserModel)
        .join(FollowModel, FollowModel.following_id == UserModel.id)
        .where(FollowModel.follower_id == current_user.id)
        .order_by(desc(FollowModel.created_at))
    )
    return list(result.scalars().all())


@router.get("/videos", response_model=List[Video])
async def get_my_videos(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """我的投稿"""
    result = await db.execute(
        select(VideoModel)
        .where(VideoModel.uploader_id == current_user.id)
        .order_by(desc(VideoModel.created_at))
    )
    return list(result.scalars().all())


@router.get("/{user_id}", response_model=User)
async def get_user_public(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取指定用户的公开信息"""
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/{user_id}/videos", response_model=List[Video])
async def get_user_videos(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取指定用户上传的视频"""
    result = await db.execute(
        select(VideoModel)
        .where(VideoModel.uploader_id == user_id)
        .order_by(desc(VideoModel.created_at))
    )
    return list(result.scalars().all())
