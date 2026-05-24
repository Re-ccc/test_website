from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey("videos.id"), index=True)
    parent_id = Column(Integer, ForeignKey("comments.id"))
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String(50))
    avatar_url = Column(String(255))
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
