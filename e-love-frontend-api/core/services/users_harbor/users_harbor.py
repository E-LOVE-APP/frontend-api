"""
Service that unloads all users in our DB to the external microservices;
Use case example:
    - Our AI-service needs to get all users from our DB to make some predictions. 
      It calls this service each time it needs to get all users. (each 6 hours in our case)
"""

import logging

from core.db.models.users.users import User
from core.services.users.users import UserService
from exceptions.exception_handler import ExceptionHandler
from utils.custom_pagination import Paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
Module that unloads all users in our DB to the external microservices;
"""


class UsersHarborService:
    """Service class to manage users in our DB."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.users_service = UserService(db_session)

    # Maybe we will modify this method later;
    async def get_all_users(self, limit: int, next_token: Optional[str]) -> List[User]:
        """
        Get all users from our DB with pagination support.
        :param limit: Number of records per page.
        :return: List of user objects.
        :raises HTTPException: If a database error occurs.
        """
        try:
            users = await self.users_service.get_users_list(limit, next_token)
            return users
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            ExceptionHandler(e)
