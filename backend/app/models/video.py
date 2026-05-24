from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bvid = Column(String(20), unique=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    cover_url = Column(String(255))
    video_url = Column(String(255))
    duration = Column(Integer)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    coin_count = Column(Integer, default=0)
    collect_count = Column(Integer, default=0)
    danmaku_count = Column(Integer, default=0)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String(500), default="")
    uploader_name = Column(String(50))
    uploader_avatar = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    uploader = relationship("User")
