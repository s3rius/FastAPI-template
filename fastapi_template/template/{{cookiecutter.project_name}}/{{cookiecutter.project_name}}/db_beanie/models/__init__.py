"""{{cookiecutter.project_name}} models."""

{%- if cookiecutter.add_dummy == "True" %}
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
{%- endif %}

from beanie import Document
from typing import Type, Sequence

def load_all_models() -> Sequence[Type[Document]]:
    """Load all models from this folder.""" # noqa: DAR201
    return [
{%- if cookiecutter.add_dummy == "True" %}
        DummyModel,
{%- endif %}
    ]
