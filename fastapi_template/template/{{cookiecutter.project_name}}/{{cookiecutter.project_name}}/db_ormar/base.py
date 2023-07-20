from ormar import ModelMeta
from {{cookiecutter.project_name}}.db.config import database
from {{cookiecutter.project_name}}.db.meta import meta


class BaseMeta(ModelMeta):
    """Base metadata for models."""

    database = database
    metadata = meta
