import uuid
from typing import Any, Dict, Optional, Tuple, Type, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm.attributes import InstrumentedAttribute
from src.services.db.db_meta import meta


@as_declarative(metadata=meta)
class Base:
    """
    Base class for all models

    It has some very cool methods which allows you
    to ship autocompletion and type verification to SQLAlchemy models.

    >>> class Model(Base):
    >>>     name = sa.Column(sa.String())
    >>>
    >>>     @classmethod
    >>>     def get_by_name(cls, name: str) -> sa.sql.Select:
    >>>         return Model.select_query(cls.id).where(cls.name == name)
    ...
    >>> session.fetchall(Model.get_by_name("random_name"))

    `id`, `created_at` and `updated_at` columns are created
    automatically for all models.

    Basic settings form models such as `__name__`, `__table__` and `__table_args__`
    defined with types to allow mypy verify this data.

    `__tablename__` generated automatically based on class name.
    """

    __name__: str
    __table__: sa.Table
    __table_args__: Tuple[Any, ...]

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    @declared_attr
    def id(self) -> Any:
        return sa.Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4
        )

    @declared_attr
    def created_at(self) -> Any:
        return sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        )

    @declared_attr
    def updated_at(self) -> Any:
        return sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            onupdate=sa.text("clock_timestamp()"),
            nullable=False,
        )

    @classmethod
    def get(
        cls, pk: Union[uuid.UUID, str], *fields: InstrumentedAttribute
    ) -> Optional[Any]:
        return cls.select_query(*fields).where(cls.id == pk)

    @classmethod
    def exists(cls, pk: Union[uuid.UUID, str]) -> sa.sql.expression.Exists:
        return sa.exists().where(cls.id == pk)

    @classmethod
    def delete(cls, pk: uuid.UUID) -> sa.sql.Delete:
        return cls.delete_query().where(cls.id == pk)

    @classmethod
    def select_query(
        cls,
        *columns: Union[InstrumentedAttribute, Type["Base"]],
        use_labels: bool = False,
    ) -> sa.sql.Select:
        return sa.select(columns or [cls], use_labels=use_labels)

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
