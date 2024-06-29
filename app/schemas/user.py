from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    social_id: str
    social_provider: str
    name: Optional[str] = None
    profile_image_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True
