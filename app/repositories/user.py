from uuid import UUID, uuid4
from typing import List

from app.models import User


class UserRepository:
    def __init__(self):
        self.users = [
            User(
                id=uuid4(),
                email="user1@example.com",
                social_id="12345",
                social_provider="google",
                name="User One",
                profile_image_url="https://example.com/user1.jpg"
            ),
            User(
                id=uuid4(),
                email="user2@example.com",
                social_id="67890",
                social_provider="facebook",
                name="User Two",
                profile_image_url="https://example.com/user2.jpg"
            )
        ]

    async def get_all(self) -> List[User]:
        return self.users
