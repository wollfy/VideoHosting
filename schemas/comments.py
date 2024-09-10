from pydantic import BaseModel
from datetime import  datetime

class Comment(BaseModel):
    id : int
    video_id : int
    user_id : int
    text : str
    created_at: datetime

class CommentCreate(BaseModel):
    text: str


class CommentUpdate(Comment):
    pass
