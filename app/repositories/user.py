from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
import app.utils.repo_utils as utils


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: dict) -> User:
        return await utils.create_record(self.db, User, user)

    async def get_users(self, page: int, limit: int) -> List[User] | None:
        return await utils.get_record_list(
            self.db,
            User,
            page,
            limit,
        )

    async def get_user_by_social_id(self, social_id: int) -> User | None:
        return await utils.get_record(self.db, User, {"social_id": social_id})
