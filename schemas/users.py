from pydantic import EmailStr, BaseModel, UUID4
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    password: str  # hashed password
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(User):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    avatar: str


class Token(BaseModel):
    id: int
    token: str


class TokenPayload(BaseModel):
    user_id: int = None