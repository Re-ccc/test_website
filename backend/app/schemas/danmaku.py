from datetime import datetime
from pydantic import BaseModel

class DanmakuBase(BaseModel):
    content: str
    time: float
    color: str = "#FFFFFF"
    type: str = "scroll"

class DanmakuCreate(DanmakuBase):
    video_id: int

class Danmaku(DanmakuBase):
    id: int
    video_id: int
    user_id: int | None = None
    username: str | None = None
    send_time: datetime
    
    class Config:
        from_attributes = True
