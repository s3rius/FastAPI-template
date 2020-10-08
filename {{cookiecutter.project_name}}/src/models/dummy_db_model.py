import uuid
from typing import Optional, List

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
{% if cookiecutter.pg_driver == "aiopg" -%}
from src.services.db import Base, db_engine
{% else %}
from src.services.db import Base
from asyncpgsa import pg
from asyncpg import Record
{% endif %}

class DummyDBModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)

    @classmethod
    async def create(
            cls,
            *,
            name: str,
            surname: str,
    ) -> None:
        query = cls.insert_query(
            name=name,
            surname=surname,
        )
        {% if cookiecutter.pg_driver == "aiopg" -%}
        async with db_engine.client.acquire() as conn:
            await conn.execute(query)
        {% else %}
        await pg.execute(query)
        {% endif %}



    @classmethod
    async def delete(cls, dummy_id: uuid.UUID) -> None:
        query = cls.delete_query().where(cls.id == dummy_id)
        {% if cookiecutter.pg_driver == "aiopg" -%}
        async with db_engine.client.acquire() as conn:
            await conn.execute(query)
        {% else %}
        await pg.fetchrow(query)
        {% endif %}

    @classmethod
    async def update(cls,
                     dummy_id: uuid.UUID,
                     *,
                     name: Optional[str] = None,
                     surname: Optional[str] = None
                     ) -> None:
        new_values = {}
        if name:
            new_values[cls.name] = name
        if surname:
            new_values[cls.surname] = surname
        query = cls.update_query().where(cls.id == dummy_id).values(new_values)
        {% if cookiecutter.pg_driver == "aiopg" -%}
        async with db_engine.client.acquire() as conn:
            await conn.execute(query)
        {% else %}
        await pg.fetchrow(query)
        {% endif %}

    @classmethod
    async def filter(cls, *,
                     dummy_id: Optional[uuid.UUID] = None,
                     name: Optional[str] = None,
                     surname: Optional[str] = None
                     ) -> {% if cookiecutter.pg_driver == "aiopg" -%}List["DummyDBModel"]{% else %}List[Record]{% endif %}:
        query = cls.select_query()
        if dummy_id:
            query = query.where(cls.id == dummy_id)
        if name:
            query = query.where(cls.name == name)
        if surname:
            query = query.where(cls.surname == surname)
        {% if cookiecutter.pg_driver == "aiopg" -%}
        async with db_engine.client.acquire() as conn:
            cursor = await conn.execute(query)
            return await cursor.fetchall()
        {% else %}
        return await pg.fetch(query)
        {% endif %}
