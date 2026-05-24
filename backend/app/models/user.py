from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50))
    avatar_url = Column(String(255))
    signature = Column(Text)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
