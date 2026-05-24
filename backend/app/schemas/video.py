from datetime import datetime
from pydantic import BaseModel

class VideoBase(BaseModel):
    title: str
    description: str | None = None
    cover_url: str | None = None
    video_url: str | None = None
    duration: int | None = None
    tags: str = ""


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    bvid: str | None = None
    view_count: int
    like_count: int
    coin_count: int
    collect_count: int
    danmaku_count: int
    uploader_id: int | None = None
    uploader_name: str | None = None
    uploader_avatar: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class VideoLikeResponse(BaseModel):
    success: bool
    liked: bool
    like_count: int


class VideoCollectResponse(BaseModel):
    success: bool
    collected: bool
    collect_count: int
