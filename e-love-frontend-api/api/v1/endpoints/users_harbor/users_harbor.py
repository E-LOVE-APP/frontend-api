from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.users.user_schema import UserOutput, UsersListResponse
from core.services.users.users import UserService
from core.services.users_harbor.users_harbor import UsersHarborService

router = APIRouter(
    prefix="/users-harbor",
)


@router.get(
    "/",
    response_model=UsersListResponse,
    responses={
        200: {
            "description": "Get all users.",
            "model": UsersListResponse,
        },
        500: {
            "description": "Server error.",
            "model": HTTPError,
        },
    },
    tags=["Users Harbor", "Get all users"],
    dependencies=[
        # TODO: change after supabase integration
        # Depends(authenticator.authenticate),
        # Depends(authenticator.require_role("Admin")),
    ],
)
async def get_all_users(
    limit: int,
    next_token: str = None,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get all users from our DB with pagination support.

    - **limit**: Number of records per page
    - **next_token**: Token to get the next page
    """
    user_service_instance = UserService(db)
    users_harbor_service = UsersHarborService(db, user_service_instance)
    return await users_harbor_service.get_all_users(limit, next_token)
