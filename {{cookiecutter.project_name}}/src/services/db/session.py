from typing import Any, List, AsyncGenerator

from aiopg.sa import SAConnection

from src.services.db import db_engine


class Session:
    def __init__(self, connection: SAConnection):
        self.connection = connection

    async def execute(self, query: Any) -> Any:
        return await self.connection.execute(query)

    async def fetchone(self, query: Any) -> Any:
        cursor = await self.connection.execute(query)
        return cursor.fetchone()

    async def scalar(self, query: Any) -> Any:
        result = await self.fetchone(query)
        return result[0]

    async def fetchall(self, query: Any) -> List[Any]:
        cursor = await self.connection.execute(query)
        return await cursor.fetchall()


async def db_session() -> AsyncGenerator[Session, None]:
    connection = await db_engine.client.acquire()
    session = Session(connection)
    try:
        yield session
    finally:
        await connection.close()
