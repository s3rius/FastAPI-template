{% if cookiecutter.add_dummy_model == "True" -%}
from src.models.dummy_db_model import DummyDBModel

__all__ = ["DummyDBModel"]
{% endif %}