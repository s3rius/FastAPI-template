from typing import Optional

from aiopg.sa import Engine, create_engine
from sqlalchemy.engine.url import URL, make_url

from src.settings import settings

db_url = make_url(
    str(URL(
        drivername=settings.db_driver,
        username=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
    ))
)


class DBEngine:
    def __init__(self, connection_url: str) -> None:
        self.dsn = connection_url
        self.engine: Optional[Engine] = None

    async def connect(self) -> None:
        self.engine = await create_engine(dsn=self.dsn)

    @property
    def client(self) -> Engine:
        if self.engine is None:
            raise ValueError("Not connected to database")
        return self.engine

    async def close(self) -> None:
        if self.engine:
            self.engine.close()
            await self.engine.wait_closed()
        raise Exception("Not connected to database")


db_engine = DBEngine(str(db_url))
