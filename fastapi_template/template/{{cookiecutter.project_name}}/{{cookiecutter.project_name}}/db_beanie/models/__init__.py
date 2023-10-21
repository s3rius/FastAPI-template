"""{{cookiecutter.project_name}} models."""

{%- if cookiecutter.add_dummy == "True" %}
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
{%- endif %}


def load_all_models(): # type: ignore
    """Load all models from this folder.""" # noqa: DAR201
    return [
{%- if cookiecutter.add_dummy == "True" %}
        DummyModel, # type: ignore
{%- endif %}
    ]
