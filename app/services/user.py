from typing import List
from app.repositories.user import UserRepository
from app.schemas.user import ResponseUserDto


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_users(self, pagination: tuple[int, int]) -> List[ResponseUserDto]:
        page, limit = pagination
        records = await self.repo.get_users(page, limit)
        return [ResponseUserDto(**record.__dict__) for record in records]
