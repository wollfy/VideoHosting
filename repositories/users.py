# users_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models.users import User
from schemas.users import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        try:
            db_user = User(username=user.username, email=user.email, password=user.password)
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to create user: {e}")

    async def get_user(self, user_id: int) -> User:
        try:
            result = await self.session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            return user
        except Exception as e:
            raise Exception(f"Failed to get user: {e}")

    async def get_all_users(self) -> list[User]:
        try:
            result = await self.session.execute(select(User))
            users = result.scalars().all()
            return users
        except Exception as e:
            raise Exception(f"Failed to get all users: {e}")

    async def update_user(self, user_id: int, user: UserUpdate) -> User:
        try:
            db_user = await self.get_user(user_id)
            if db_user:
                db_user.username = user.username
                db_user.email = user.email
                await self.session.commit()
                await self.session.refresh(db_user)
            return db_user
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to update user: {e}")

    async def delete_user(self, user_id: int) -> bool:
        try:
            db_user = await self.get_user(user_id)
            if db_user:
                await self.session.delete(db_user)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Failed to delete user: {e}")