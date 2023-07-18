from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String
from {{cookiecutter.project_name}}.db.base import Base


class DummyModel(Base):
    """Model for demo purpose."""

    __tablename__ = "dummy_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
