
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.rdb import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)
