# likes_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models.likes import Like
from schemas.likes import LikeCreate

class LikesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_like(self, like: LikeCreate) -> Like:
        try:
            db_like = Like(video_id=like.video_id, user_id=like.user_id)
            self.session.add(db_like)
            await self.session.commit()
            await self.session.refresh(db_like)
            return db_like
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to create like: {e}")

    async def get_like(self, like_id: int) -> Like:
        try:
            result = await self.session.execute(select(Like).where(Like.id == like_id))
            like = result.scalars().first()
            return like
        except Exception as e:
            raise Exception(f"Failed to get like: {e}")

    async def get_all_likes(self) -> list[Like]:
        try:
            result = await self.session.execute(select(Like))
            likes = result.scalars().all()
            return likes
        except Exception as e:
            raise Exception(f"Failed to get all likes: {e}")

    async def delete_like(self, like_id: int) -> bool:
        try:
            db_like = await self.get_like(like_id)
            if db_like:
                await self.session.delete(db_like)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to delete like: {e}")