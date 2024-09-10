# comments_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models.comments import Comment
from schemas.comments import CommentCreate, CommentUpdate

class CommentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_comment(self, comment: CommentCreate) -> Comment:
        try:
            db_comment = Comment(video_id=comment.video_id, user_id=comment.user_id, text=comment.text)
            self.session.add(db_comment)
            await self.session.commit()
            await self.session.refresh(db_comment)
            return db_comment
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to create comment: {e}")

    async def get_comment(self, comment_id: int) -> Comment:
        try:
            result = await self.session.execute(select(Comment).where(Comment.id == comment_id))
            comment = result.scalars().first()
            return comment
        except Exception as e:
            raise Exception(f"Failed to get comment: {e}")

    async def get_all_comments(self) -> list[Comment]:
        try:
            result = await self.session.execute(select(Comment))
            comments = result.scalars().all()
            return comments
        except Exception as e:
            raise Exception(f"Failed to get all comments: {e}")

    async def delete_comment(self, comment_id: int) -> bool:
        try:
            db_comment = await self.get_comment(comment_id)
            if db_comment:
                await self.session.delete(db_comment)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to delete like: {e}")