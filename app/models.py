from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class User(BaseModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    social_id: Mapped[str] = mapped_column(String, unique=True)
    social_provider: Mapped[str] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String)
    profile_image_url: Mapped[Optional[str]] = mapped_column(String)
