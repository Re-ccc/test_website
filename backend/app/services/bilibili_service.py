import httpx
from typing import List
from app.schemas.video import Video

class BilibiliService:
    BASE_URL = "https://api.bilibili.com"
    
    async def get_home_feed(self) -> List[Video]:
        url = f"{self.BASE_URL}/x/web-interface/index/top/feed/rcmd"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={
                    "ps": 20,
                    "fresh_type": 3
                })
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_videos(data)
        except Exception:
            pass
        return []
    
    async def get_ranking(self, type: str = "all") -> List[Video]:
        url = f"{self.BASE_URL}/x/web-interface/ranking/v2"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={"rid": 0})
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_ranking(data)
        except Exception:
            pass
        return []
    
    async def get_video_detail(self, bvid: str) -> Video | None:
        url = f"{self.BASE_URL}/x/web-interface/view"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={"bvid": bvid})
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_video_detail(data)
        except Exception:
            pass
        return None
    
    def _parse_videos(self, data: dict) -> List[Video]:
        videos = []
        if data.get("code") == 0 and data.get("data"):
            for item in data["data"].get("list", []):
                video = Video(
                    id=item.get("id", 0),
                    bvid=item.get("bvid", ""),
                    title=item.get("title", ""),
                    description=item.get("desc", ""),
                    cover_url=item.get("pic", ""),
                    duration=item.get("duration", 0),
                    view_count=item.get("play", 0),
                    like_count=item.get("like", 0),
                    coin_count=item.get("coin", 0),
                    collect_count=item.get("favorite", 0),
                    danmaku_count=item.get("danmaku", 0),
                    uploader_name=item.get("owner", {}).get("name", ""),
                    uploader_avatar=item.get("owner", {}).get("face", ""),
                    created_at=item.get("pubdate", "")
                )
                videos.append(video)
        return videos
    
    def _parse_ranking(self, data: dict) -> List[Video]:
        videos = []
        if data.get("code") == 0 and data.get("data"):
            for item in data["data"].get("list", []):
                video = Video(
                    id=item.get("id", 0),
                    bvid=item.get("bvid", ""),
                    title=item.get("title", ""),
                    description=item.get("desc", ""),
                    cover_url=item.get("pic", ""),
                    duration=item.get("duration", 0),
                    view_count=item.get("play", 0),
                    like_count=item.get("like", 0),
                    coin_count=item.get("coin", 0),
                    collect_count=item.get("favorite", 0),
                    danmaku_count=item.get("danmaku", 0),
                    uploader_name=item.get("owner", {}).get("name", ""),
                    uploader_avatar=item.get("owner", {}).get("face", ""),
                    created_at=item.get("pubdate", "")
                )
                videos.append(video)
        return videos
    
    def _parse_video_detail(self, data: dict) -> Video | None:
        if data.get("code") == 0 and data.get("data"):
            item = data["data"]
            return Video(
                id=item.get("aid", 0),
                bvid=item.get("bvid", ""),
                title=item.get("title", ""),
                description=item.get("desc", ""),
                cover_url=item.get("pic", ""),
                duration=item.get("duration", 0),
                view_count=item.get("stat", {}).get("view", 0),
                like_count=item.get("stat", {}).get("like", 0),
                coin_count=item.get("stat", {}).get("coin", 0),
                collect_count=item.get("stat", {}).get("favorite", 0),
                danmaku_count=item.get("stat", {}).get("danmaku", 0),
                uploader_name=item.get("owner", {}).get("name", ""),
                uploader_avatar=item.get("owner", {}).get("face", ""),
                created_at=item.get("pubdate", "")
            )
        return None
