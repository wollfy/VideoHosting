from pydantic import BaseModel

class Like(BaseModel):
    id: int
    video_id: int
    user_id: int
    created_at: str

class LikeCreate(BaseModel):
    pass  # no fields needed for like creation