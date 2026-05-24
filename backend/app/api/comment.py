from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.comment import Comment as CommentModel
from app.models.comment_like import CommentLike as CommentLikeModel
from app.models.user import User as UserModel
from app.schemas.comment import Comment, CommentCreate

router = APIRouter()

@router.get("/video/{video_id}", response_model=List[Comment])
async def get_comments(video_id: int, db: AsyncSession = Depends(get_db)):
    """获取视频评论（包含回复）- 两次查询避免 N+1"""
    # 一次查出所有父评论和回复
    result = await db.execute(
        select(CommentModel)
        .where(CommentModel.video_id == video_id)
        .order_by(desc(CommentModel.created_at))
        .limit(200)
    )
    all_comments = result.scalars().all()

    # 在内存中分离父评论和回复
    parents = []
    replies_by_parent: dict = {}
    for c in all_comments:
        if c.parent_id is None:
            parents.append(c)
        else:
            replies_by_parent.setdefault(c.parent_id, []).append(c)

    def to_schema(c: CommentModel) -> Comment:
        item_replies = replies_by_parent.get(c.id, [])
        item_replies.sort(key=lambda r: r.created_at)
        return Comment(
            id=c.id,
            video_id=c.video_id,
            parent_id=c.parent_id,
            content=c.content,
            user_id=c.user_id,
            username=c.username,
            avatar_url=c.avatar_url,
            like_count=c.like_count,
            created_at=c.created_at,
            replies=[to_schema(r) for r in item_replies[:10]]
        )

    return [to_schema(p) for p in parents[:50]]

@router.post("", response_model=Comment)
async def create_comment(
    comment: CommentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发表评论"""
    new_comment = CommentModel(
        video_id=comment.video_id,
        parent_id=comment.parent_id,
        content=comment.content,
        user_id=current_user.id,
        username=current_user.nickname,
        avatar_url=current_user.avatar_url or "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return Comment(
        id=new_comment.id,
        video_id=new_comment.video_id,
        parent_id=new_comment.parent_id,
        content=new_comment.content,
        user_id=new_comment.user_id,
        username=new_comment.username,
        avatar_url=new_comment.avatar_url,
        like_count=new_comment.like_count,
        created_at=new_comment.created_at,
        replies=[]
    )

@router.post("/{comment_id}/like")
async def like_comment(
    comment_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """点赞/取消点赞评论"""
    result = await db.execute(select(CommentModel).where(CommentModel.id == comment_id))
    comment = result.scalars().first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    existing = await db.execute(
        select(CommentLikeModel).where(
            and_(
                CommentLikeModel.user_id == current_user.id,
                CommentLikeModel.comment_id == comment_id,
            )
        )
    )
    like = existing.scalars().first()

    if like:
        await db.delete(like)
        comment.like_count = max(0, comment.like_count - 1)
        await db.commit()
        return {"success": True, "liked": False, "like_count": comment.like_count}

    new_like = CommentLikeModel(user_id=current_user.id, comment_id=comment_id)
    db.add(new_like)
    comment.like_count += 1
    await db.commit()
    return {"success": True, "liked": True, "like_count": comment.like_count}
