from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
import app.utils.repo_utils as utils


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: dict) -> User:
        return await utils.create_record(self.db, User, user)

    async def get_users(self, page: int, limit: int) -> Union[List[User], None]:
        return await utils.get_record_list(
            self.db,
            User,
            page,
            limit,
        )

    async def get_user_by_social_id(self, social_id: int) -> Union[User, None]:
        return await utils.get_record(self.db, User, {"social_id": social_id})
