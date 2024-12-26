from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import authenticator
from configuration.database import get_db_session

from core.db.models.users.users import User
from core.services.users.users import UserService


async def get_current_user(
    payload: dict = Depends(authenticator.authenticate),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Get the current user.

    :param payload: Payload from the token
    :param db: Database session
    :return: User object
    :raises HTTPException: If user not found
    """
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No sub found in token",
        )

    # TODO: extract to params?
    user_service = UserService(db)
    user = await user_service.get_user_by_supabase_id(sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in local DB",
        )
    return user
