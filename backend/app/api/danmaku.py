from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.danmaku import Danmaku as DanmakuModel
from app.models.user import User as UserModel
from app.schemas.danmaku import Danmaku, DanmakuCreate

router = APIRouter()

@router.get("/video/{video_id}", response_model=List[Danmaku])
async def get_danmakus(video_id: int, db: AsyncSession = Depends(get_db)):
    """获取视频弹幕"""
    result = await db.execute(
        select(DanmakuModel)
        .where(DanmakuModel.video_id == video_id)
        .order_by(DanmakuModel.time)
        .limit(200)
    )
    danmakus = result.scalars().all()
    return list(danmakus)

@router.post("", response_model=Danmaku)
async def send_danmaku(
    danmaku: DanmakuCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送弹幕"""
    new_danmaku = DanmakuModel(
        video_id=danmaku.video_id,
        content=danmaku.content,
        time=danmaku.time,
        color=danmaku.color,
        type=danmaku.type,
        user_id=current_user.id,
        username=current_user.nickname
    )
    db.add(new_danmaku)

    # 更新视频弹幕数
    from app.models.video import Video as VideoModel
    result = await db.execute(select(VideoModel).where(VideoModel.id == danmaku.video_id))
    video = result.scalars().first()
    if video:
        video.danmaku_count = (video.danmaku_count or 0) + 1

    await db.commit()
    await db.refresh(new_danmaku)
    return new_danmaku
