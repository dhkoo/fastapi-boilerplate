from fastapi import APIRouter, Depends, status
from app.dependencies import get_user_service
from app.schemas.user import ResponseUserList
from app.services.user import UserService
from app.utils.api_utils import pagination_query

router = APIRouter(tags=["user"])


@router.get("/users", response_model=ResponseUserList)
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    pagination: tuple[int, int] = Depends(pagination_query),
):
    data = await user_service.get_users(pagination)
    return ResponseUserList(
        code=status.HTTP_200_OK, message="success", data=data
    )
