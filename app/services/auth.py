import os
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
import requests

from app.repositories.user import UserRepository

load_dotenv()

CLERK_API_URL = os.getenv("CLERK_API_URL")
CLERK_API_KEY = os.getenv("CLERK_API_KEY")
CLERK_PEM_PUBLIC_KEY = os.getenv('CLERK_PEM_PUBLIC_KEY').replace('\\n', '\n')


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository
    ):
        self.user_repository = user_repository

    async def verify_token(self, token: str):
        try:
            payload = jwt.decode(
                token, key=CLERK_PEM_PUBLIC_KEY, algorithms=['RS256'])
            clerk_user_id = payload.get("sub")
            user_record = await self.user_repository.get_user_by_social_id(clerk_user_id)

            if user_record is None:
                user_info = await self.fetch_user_info(clerk_user_id)
                user_dict = {
                    "social_id": clerk_user_id,
                    "email": user_info.get("email_addresses")[0].get("email_address"),
                    "social_provider": "clerk"
                }
                user_record = await self.user_repository.create_user(user_dict)

            return user_record.id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def fetch_user_info(self, user_id: str):
        response = requests.get(
            f"{CLERK_API_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {CLERK_API_KEY}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Error fetching user info from Clerk")
        return response.json()
