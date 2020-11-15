from typing import Any, List, AsyncGenerator

from aiopg.sa import SAConnection

from src.services.db import db_engine


class Session:
    """
    Database session object.
    It used to acquire connection from pool
    and execute many queries using one connection.
    """
    def __init__(self, connection: SAConnection):
        self.connection = connection

    async def execute(self, query: Any) -> Any:
        """
        Simply execute SQLAlchemy generated query
        or string query and return raw results.
        """
        return await self.connection.execute(query)

    async def fetchone(self, query: Any) -> Any:
        """
        Get one object from database by query.
        """
        cursor = await self.connection.execute(query)
        return await cursor.fetchone()

    async def scalar(self, query: Any) -> Any:
        """
        Scalar returns first column of the first result.
        It's convenient fot such things as getting function result.

        >>> session = Session(connection)
        >>> session.scalar(Model.insert_query(**values).returning(Model.id))
        UUID('7a9ffbfe-f871-42fb-a371-7bd29227a9ff')
        """
        result = await self.fetchone(query)
        return result[0]

    async def fetchall(self, query: Any) -> List[Any]:
        """
        Get all matching objects from database by query.
        """
        cursor = await self.connection.execute(query)
        return await cursor.fetchall()


async def db_session() -> AsyncGenerator[Session, None]:
    """
    Dependency to acquire connection from database pool
    and close it when handler function is proceeds.
    """
    connection = await db_engine.client.acquire()
    session = Session(connection)
    try:
        yield session
    finally:
        await connection.close()
