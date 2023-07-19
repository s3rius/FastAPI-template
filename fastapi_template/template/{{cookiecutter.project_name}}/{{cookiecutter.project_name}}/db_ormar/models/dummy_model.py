import ormar
from {{cookiecutter.project_name}}.db.base import BaseMeta


class DummyModel(ormar.Model):
    """Model for demo purpose."""

    class Meta(BaseMeta):
        tablename = "dummy_model"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)  # noqa: WPS432
