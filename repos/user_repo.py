from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from repos.base_repo import BaseRepository
from users.models import User


class UserRepository(BaseRepository):
    table = User

    @classmethod
    async def get_user_by_username(
        cls, username: str, session: AsyncSession
    ) -> Result[User]:
        query = select(cls.table).where(cls.table.username == username)
        user = await session.execute(query)
        return user.scalar_one_or_none()

    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession) -> Result[User]:
        query = select(cls.table).where(cls.table.email == email)
        user = await session.execute(query)
        return user.scalar_one_or_none()
