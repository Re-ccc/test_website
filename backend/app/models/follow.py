from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

class Follow(Base):
    __tablename__ = "follows"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey("users.id"), index=True)
    following_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='uk_follower_following'),
    )
