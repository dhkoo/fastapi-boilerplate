from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
import app.utils.repo_utils as utils


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_users(self, page: int, limit: int) -> List[User] | None:
        return await utils.get_record_list(
            self.db,
            User,
            page,
            limit,
        )
