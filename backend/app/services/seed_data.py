"""数据库种子数据初始化"""
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.models.video import Video as VideoModel
from app.models.danmaku import Danmaku as DanmakuModel
from app.models.comment import Comment as CommentModel
from app.models.like import Like as LikeModel
from app.services.data_templates import USER_NAMES, VIDEO_TITLES, COMMENT_TEMPLATES, DANMAKU_TEMPLATES

async def init_seed_data(db: AsyncSession):
    """初始化种子数据"""
    # 检查是否已有数据
    result = await db.execute(select(func.count(VideoModel.id)))
    count = result.scalar()
    if count > 0:
        print(f"数据库已有 {count} 条视频数据，跳过初始化")
        return
    
    print("开始初始化种子数据...")
    
    # 1. 创建默认用户
    default_user = UserModel(
        username="default",
        password_hash=get_password_hash("123456"),
        nickname="默认用户",
        signature="这个人很懒，什么都没留下",
        follower_count=0,
        following_count=0
    )
    db.add(default_user)
    await db.flush()
    
    # 创建一些随机用户
    users = [default_user]
    for i, name in enumerate(USER_NAMES):
        user = UserModel(
            username=f"user{i+1}",
            password_hash=get_password_hash("123456"),
            nickname=name,
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed=user{i+1}",
            signature="这个人很懒，什么都没留下",
            follower_count=random.randint(0, 50000),
            following_count=random.randint(0, 500)
        )
        db.add(user)
        users.append(user)
    await db.flush()
    
    # 2. 创建视频
    videos = []
    used_titles = set()
    for i in range(30):
        title = random.choice(VIDEO_TITLES)
        while title in used_titles:
            title = random.choice(VIDEO_TITLES)
        used_titles.add(title)
        
        uploader = random.choice(USER_NAMES)
        view = random.randint(5000, 2000000)
        like = random.randint(int(view * 0.02), int(view * 0.15))
        
        video = VideoModel(
            bvid=f"BV{i+1:06d}",
            title=title,
            description=f"这是[{title}]的视频内容，点击观看了解更多精彩内容！记得点赞关注！",
            cover_url=f"https://picsum.photos/640/360?random={i+1}",
            video_url="https://www.w3schools.com/html/mov_bbb.mp4",
            duration=random.randint(120, 1800),
            view_count=view,
            like_count=like,
            coin_count=random.randint(int(like * 0.1), int(like * 0.5)),
            collect_count=random.randint(int(like * 0.2), int(like * 0.8)),
            danmaku_count=0,
            uploader_id=random.choice(users).id,
            uploader_name=uploader,
            uploader_avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={uploader}",
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        db.add(video)
        videos.append(video)
    await db.flush()
    
    # 3. 创建弹幕（每个视频50条）
    for video in videos:
        for j in range(50):
            danmaku = DanmakuModel(
                video_id=video.id,
                content=random.choice(DANMAKU_TEMPLATES),
                time=round(random.uniform(0, 600), 2),
                color=random.choice(["#FFFFFF", "#FF0000", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF"]),
                type=random.choice(["scroll", "scroll", "scroll", "top", "bottom"]),
                user_id=random.choice(users).id,
                username=random.choice(USER_NAMES),
                send_time=datetime.now()
            )
            db.add(danmaku)
        
        # 更新视频弹幕数
        video.danmaku_count = 50
    
    await db.flush()
    
    # 4. 创建评论（每个视频20条，含回复）
    for video in videos:
        for j in range(20):
            comment = CommentModel(
                video_id=video.id,
                content=random.choice(COMMENT_TEMPLATES),
                user_id=random.choice(users).id,
                username=random.choice(USER_NAMES),
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed=comment{j}",
                like_count=random.randint(0, 500),
                created_at=datetime.now() - timedelta(hours=random.randint(0, 72))
            )
            db.add(comment)
            await db.flush()
            
            # 50%概率加回复
            if random.random() > 0.5:
                for k in range(random.randint(1, 4)):
                    reply = CommentModel(
                        video_id=video.id,
                        parent_id=comment.id,
                        content=random.choice(["同意！", "说得好", "+1", "哈哈哈", "赞同", "确实"]),
                        user_id=random.choice(users).id,
                        username=random.choice(USER_NAMES),
                        avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed=reply{j}{k}",
                        like_count=random.randint(0, 50),
                        created_at=datetime.now() - timedelta(hours=random.randint(0, 48))
                    )
                    db.add(reply)
    
    await db.commit()
    print(f"初始化完成: {len(videos)} 个视频, 用户, 弹幕, 评论")
