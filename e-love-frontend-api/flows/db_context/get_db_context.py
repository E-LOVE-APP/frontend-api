# db_flow.py
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import AsyncSessionLocal, handle_session_exception

logger = logging.getLogger(__name__)


class DbSessionContext:
    """
    Контекстный менеджер для Prefect flow (или любого другого кода),
    где нужно писать:

        async with DbSessionContext() as session:
            ...

    """

    def __init__(self):
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await handle_session_exception(self.session, exc_val)
        await self.session.close()


def create_db_context() -> DbSessionContext:
    """
    Просто фабрика, чтобы писать:

      async with create_db_context() as session:
          ...
    """
    return DbSessionContext()
