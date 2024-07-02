from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

from app.schemas.base import ResponseBaseModel


class ResponseUserDto(BaseModel):
    id: UUID
    email: EmailStr
    social_id: str
    social_provider: str
    name: Optional[str] = None
    profile_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ResponseUser(ResponseBaseModel):
    data: ResponseUserDto


class ResponseUserList(ResponseBaseModel):
    data: list[ResponseUserDto]
