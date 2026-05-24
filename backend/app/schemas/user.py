from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    nickname: str | None = None
    avatar_url: str | None = None
    signature: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    signature: str | None = None

class User(BaseModel):
    id: int
    username: str
    nickname: str | None = None
    avatar_url: str | None = None
    signature: str | None = None
    follower_count: int
    following_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
