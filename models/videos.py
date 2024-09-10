from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    description = Column(String)
    file_url = Column(String)
    upload_date = Column(DateTime)

    def __repr__(self):
        return f"Video(id={self.id}, title={self.title}, description={self.description}, file_url={self.file_url}, upload_date={self.upload_date})"