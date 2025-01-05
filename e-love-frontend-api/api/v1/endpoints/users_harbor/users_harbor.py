from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import get_db_session
from core.schemas.errors.httperror import HTTPError
from core.schemas.users.user_schema import UsersHarborListResponse
from core.services.users.users import UserService
from core.services.users_harbor.users_harbor import UsersHarborService
from exceptions.exception_handler import ExceptionHandler

router = APIRouter(
    prefix="/users-harbor",
)


@router.get(
    "/",
    response_model=UsersHarborListResponse,
    responses={
        200: {
            "description": "Get all users.",
            "model": UsersHarborListResponse,
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
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get all users from our DB with pagination support.

    - **limit**: Number of records per page
    - **next_token**: Token to get the next page
    """
    try:
        users_harbor_service = UsersHarborService(db)

        return await users_harbor_service.get_all_users()
    except Exception as e:
        ExceptionHandler(e)
        # raise HTTPError(status_code=500, detail="Server error")
