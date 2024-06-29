
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    social_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    social_provider: Mapped[str] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String)
    profile_image_url: Mapped[Optional[str]] = mapped_column(String)
