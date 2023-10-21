import logging

from core.database import async_session


class AsyncSessionManager:
    def __init__(self) -> None:
        self.session = async_session()

    async def __aenter__(self) -> async_session:
        return self.session

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        if exc_type is not None:
            logging.error(f"Exception occurred, type: {exc_type}, value: {exc_val}")
            await self.rollback()
        else:
            logging.info("Session was closed")
            await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
