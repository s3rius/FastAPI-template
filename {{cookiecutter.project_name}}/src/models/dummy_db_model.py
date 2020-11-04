import uuid
from typing import Optional

from sqlalchemy import Column, String, sql
from sqlalchemy.dialects.postgresql import UUID

from src.services.db import Base


class DummyDBModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)

    @classmethod
    def create(
            cls,
            *,
            name: str,
            surname: str,
    ) -> sql.Insert:
        return cls.insert_query(
            name=name,
            surname=surname,
        )

    @classmethod
    def delete(cls, dummy_id: uuid.UUID) -> sql.Delete:
        return cls.delete_query().where(cls.id == dummy_id)

    @classmethod
    def update(cls,
               dummy_id: uuid.UUID,
               *,
               name: Optional[str] = None,
               surname: Optional[str] = None
               ) -> sql.Update:
        new_values = {}
        if name:
            new_values[cls.name] = name
        if surname:
            new_values[cls.surname] = surname
        return cls.update_query().where(cls.id == dummy_id).values(new_values)

    @classmethod
    def filter(cls, *,
               dummy_id: Optional[uuid.UUID] = None,
               name: Optional[str] = None,
               surname: Optional[str] = None
               ) -> sql.Select:
        query = cls.select_query()
        if dummy_id:
            query = query.where(cls.id == dummy_id)
        if name:
            query = query.where(cls.name == name)
        if surname:
            query = query.where(cls.surname == surname)
        return query
