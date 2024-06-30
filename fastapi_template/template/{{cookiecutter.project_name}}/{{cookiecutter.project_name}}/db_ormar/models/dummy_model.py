import ormar
from {{cookiecutter.project_name}}.db.base import ormar_config


class DummyModel(ormar.Model):
    """Model for demo purpose."""
    ormar_config = ormar_config.copy(tablename="dummy_model")

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)  # noqa: WPS432
