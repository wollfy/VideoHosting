from datetime import datetime
from pydantic import BaseModel

class Video(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    file_url: str
    upload_date: datetime

class VideoCreate(BaseModel):
    title: str
    description: str
    file_url: str