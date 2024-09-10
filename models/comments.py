from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String, nullable=False)