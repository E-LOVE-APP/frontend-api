# clear_db.py
# не работает нихуя

import asyncio
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database import (  # Обратите внимание на импорт Base
    AsyncSessionLocal,
    Base,
    engine,
)


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(f"Database session error: {e}")
            raise


async def clear_database():
    async with engine.begin() as conn:
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        await conn.commit()
    print("Database has been successfully cleared.")


if __name__ == "__main__":
    asyncio.run(clear_database())
