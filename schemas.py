from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "patient"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserOut(UserBase):
    id: int
    username: str
    email: Optional[str]
    bio: Optional[str]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None