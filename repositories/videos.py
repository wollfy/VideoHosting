from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from schemas.videos import VideoCreate
from models.videos import Video

class VideoRepository:
    def __init__(self,session :AsyncSession):
        self.session = session

    async def create_video(self, video: VideoCreate) -> Video:
        try:
            db_video = Video(title=video.title, description=video.description, file_url=video.file_url)
            self.session.add(db_video)
            await self.session.commit()
            await self.session.refresh(db_video)
            return db_video
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to create video: {e}")
    async def get_video ( self, video_id : int) -> Video :
        try:
            result = await self.session.execute(select(Video).where(Video.id == video_id))
            video = result.scalars().first()
            return video

        except Exception as e:
            raise Exception(f"Failed to get video: {e}")

    async def get_all_videos(self) -> list[Video]:
        try:
            result = await self.session.execute(select(Video))
            videos = result.scalars().all()
            return videos
        except Exception as e:
            raise Exception(f"Failed to get all videos: {e}")

    async def update_video(self, video_id: int, video: VideoCreate) -> Video:
        try:
            db_video = await self.get_video(video_id)
            if db_video:
                db_video.title = video.title
                db_video.description = video.description
                db_video.file_url = video.file_url
                await self.session.commit()
                await self.session.refresh(db_video)
            return db_video
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to update video: {e}")

    async def delete_video(self, video_id: int) -> bool:
        try:
            db_video = await self.get_video(video_id)
            if db_video:
                await self.session.delete(db_video)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to delete video: {e}")