from sqlalchemy.orm import DeclarativeBase
from {{cookiecutter.project_name}}.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

