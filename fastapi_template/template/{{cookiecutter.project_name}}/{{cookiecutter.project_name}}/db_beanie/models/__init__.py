"""{{cookiecutter.project_name}} models."""

{%- if cookiecutter.add_dummy == "True" %}
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
{%- endif %}

from beanie import Document
from collections.abc import Sequence

def load_all_models() -> Sequence[type[Document]]:
    """Load all models from this folder."""
    return [
{%- if cookiecutter.add_dummy == "True" %}
        DummyModel,
{%- endif %}
    ]
