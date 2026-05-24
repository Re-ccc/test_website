from datetime import datetime
from pydantic import BaseModel
from typing import List

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    video_id: int
    parent_id: int | None = None

class Comment(CommentBase):
    id: int
    video_id: int
    parent_id: int | None = None
    user_id: int | None = None
    username: str | None = None
    avatar_url: str | None = None
    like_count: int
    created_at: datetime
    replies: List["Comment"] = []
    
    class Config:
        from_attributes = True

Comment.update_forward_refs()
