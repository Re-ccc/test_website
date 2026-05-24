import random
from typing import List, Optional
from datetime import datetime
from app.schemas.danmaku import Danmaku
from app.schemas.comment import Comment
from app.schemas.user import User
from app.schemas.video import Video
from app.services.data_templates import USER_NAMES, VIDEO_TITLES, COMMENT_TEMPLATES, DANMAKU_TEMPLATES

class MockService:
    def __init__(self):
        self._video_cache = {}  # bvid -> Video
        self._video_list_cache = []  # List[Video]
        self._cache_initialized = False

    def _init_cache(self):
        if self._cache_initialized:
            return
        self._cache_initialized = True

        videos = []
        used_titles = set()
        for i in range(60):
            title = random.choice(VIDEO_TITLES)
            while title in used_titles:
                title = random.choice(VIDEO_TITLES)
            used_titles.add(title)
            
            view = random.randint(1000, 1000000)
            like = random.randint(int(view * 0.01), int(view * 0.15))
            
            video = Video(
                id=i + 1,
                bvid=f"BV{i+1:06d}",
                title=title,
                description=f"这是[{title}]的视频内容，点击观看了解更多精彩内容！",
                cover_url=f"https://picsum.photos/640/360?random={i}",
                video_url=f"https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
                duration=random.randint(60, 1200),
                view_count=view,
                like_count=like,
                coin_count=random.randint(int(like * 0.1), int(like * 0.5)),
                collect_count=random.randint(int(like * 0.2), int(like * 0.8)),
                danmaku_count=random.randint(int(view * 0.01), int(view * 0.05)),
                uploader_name=random.choice(USER_NAMES),
                uploader_avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed=uploader{i}",
                created_at=datetime.now()
            )
            videos.append(video)
            self._video_cache[video.bvid] = video
        
        self._video_list_cache = videos
    
    def generate_videos(self, count: int = 20) -> List[Video]:
        self._init_cache()
        return random.sample(self._video_list_cache, min(count, len(self._video_list_cache)))
    
    def generate_ranking(self, count: int = 30) -> List[Video]:
        """热门排行榜 - 按播放量和点赞数综合排序"""
        self._init_cache()
        # 计算热度分 = view_count * 0.6 + like_count * 0.4
        ranked = sorted(
            self._video_list_cache,
            key=lambda v: v.view_count * 0.6 + v.like_count * 0.4,
            reverse=True
        )
        return ranked[:count]
    
    def search_videos(self, keyword: str) -> List[Video]:
        """搜索视频 - 按标题关键字匹配"""
        self._init_cache()
        keyword_lower = keyword.lower()
        results = [
            v for v in self._video_list_cache
            if keyword_lower in v.title.lower() or keyword_lower in (v.uploader_name or "").lower()
        ]
        return results
    
    def get_video_by_bvid(self, bvid: str) -> Optional[Video]:
        """通过bvid获取视频"""
        self._init_cache()
        video = self._video_cache.get(bvid)
        if video:
            # 返回一个新对象，防止修改影响缓存（但view_count需要实时变化）
            return video
        return None
    
    def generate_danmakus(self, video_id: int, count: int = 50) -> List[Danmaku]:
        danmakus = []
        for i in range(count):
            danmaku = Danmaku(
                id=i + 1,
                video_id=video_id,
                content=random.choice(DANMAKU_TEMPLATES),
                time=round(random.uniform(0, 600), 2),
                color=random.choice(["#FFFFFF", "#FF0000", "#00FF00", "#FFFF00", "#FF00FF"]),
                type=random.choice(["scroll", "scroll", "scroll", "top", "bottom"]),
                username=random.choice(USER_NAMES),
                send_time=datetime.now()
            )
            danmakus.append(danmaku)
        return sorted(danmakus, key=lambda x: x.time)
    
    def generate_comments(self, video_id: int, count: int = 20) -> List[Comment]:
        comments = []
        for i in range(count):
            comment = Comment(
                id=i + 1,
                video_id=video_id,
                content=random.choice(COMMENT_TEMPLATES),
                username=random.choice(USER_NAMES),
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={i}",
                like_count=random.randint(0, 500),
                created_at=datetime.now(),
                replies=self._generate_replies(i + 1) if random.random() > 0.5 else []
            )
            comments.append(comment)
        return comments
    
    def _generate_replies(self, parent_id: int) -> List[Comment]:
        replies = []
        count = random.randint(1, 5)
        for i in range(count):
            reply = Comment(
                id=parent_id * 100 + i + 1,
                video_id=0,
                parent_id=parent_id,
                content=random.choice(["同意！", "说得好", "+1", "哈哈哈"]),
                username=random.choice(USER_NAMES),
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={parent_id}{i}",
                like_count=random.randint(0, 50),
                created_at=datetime.now()
            )
            replies.append(reply)
        return replies
    
    def generate_users(self, count: int = 10) -> List[User]:
        users = []
        for i in range(count):
            user = User(
                id=i + 1,
                username=f"user{i + 1}",
                nickname=random.choice(USER_NAMES),
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed=user{i}",
                signature="这个人很懒，什么都没留下",
                follower_count=random.randint(0, 10000),
                following_count=random.randint(0, 500),
                created_at=datetime.now()
            )
            users.append(user)
        return users
