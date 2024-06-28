from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter()


def get_user_service():
    return UserService()


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    return users
