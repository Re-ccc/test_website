from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Danmaku(Base):
    __tablename__ = "danmakus"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey("videos.id"), index=True)
    content = Column(String(100), nullable=False)
    time = Column(Float, nullable=False)
    color = Column(String(10), default="#FFFFFF")
    type = Column(String(10), default="scroll")
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String(50))
    send_time = Column(DateTime, server_default=func.now())
