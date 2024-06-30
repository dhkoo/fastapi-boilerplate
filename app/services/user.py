from uuid import UUID
from typing import List
from app.models import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()
