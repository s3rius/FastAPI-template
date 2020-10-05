from typing import Any, Dict, Optional

import sqlalchemy as sa
from aiopg.sa import Engine, create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.settings import settings

db_url = make_url(
    URL(
        drivername=settings.db_driver,
        username=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
    )
)

meta = MetaData()


class DBEngine:
    def __init__(self, connection_url: str) -> None:
        self.dsn = connection_url
        self.engine: Optional[Engine] = None

    async def connect(self) -> None:
        self.engine = await create_engine(dsn=self.dsn, maxsize=100)

    @property
    def client(self) -> Engine:
        if self.engine:
            return self.engine
        raise Exception("Not connected to database")

    async def close(self) -> None:
        if self.engine:
            self.engine.close()
            await self.engine.wait_closed()


db_engine = DBEngine(str(db_url))


@as_declarative(metadata=meta)
class Base:
    """Base class for all models"""

    __name__: str
    __table__: Table

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    @declared_attr
    def created_at(self) -> sa.Column:
        return sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        )

    @declared_attr
    def updated_at(self) -> sa.Column:
        return sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            onupdate=sa.text("clock_timestamp()"),
            nullable=False,
        )

    @classmethod
    def select_query(cls, *columns: InstrumentedAttribute) -> sa.sql.Select:
        return sa.select(columns or [cls])

    @classmethod
    def insert_query(cls, **values: Any) -> sa.sql.Insert:
        return cls.__table__.insert().values(**values)

    @classmethod
    def update_query(cls) -> sa.sql.Update:
        return cls.__table__.update()

    @classmethod
    def delete_query(cls) -> sa.sql.Delete:
        return cls.__table__.delete()

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.key) for c in self.__table__.columns}
