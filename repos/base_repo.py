from typing import Unpack

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base


class BaseRepository:
    table: Base

    @classmethod
    async def insert_one(cls, session: AsyncSession, **kwargs: Unpack) -> Base:
        new_row = cls.table(**kwargs)
        session.add(new_row)
        return new_row

    @classmethod
    async def delete_one(cls, session: AsyncSession, obj_id: int) -> None:
        query = delete(cls.table).where(cls.table.id == obj_id)
        await session.execute(query)

    @classmethod
    async def update_one(
        cls, session: AsyncSession, obj_id: int, **kwargs: Unpack
    ) -> None:
        query = update(cls.table).where(cls.table.id == obj_id).values(**kwargs)
        await session.execute(query)
