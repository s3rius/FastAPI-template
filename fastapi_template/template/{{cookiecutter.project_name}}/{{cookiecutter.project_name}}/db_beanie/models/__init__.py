"""{{cookiecutter.project_name}} models."""

from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel


def load_all_models(): # type: ignore
    """Load all models from this folder.""" # noqa: DAR201
    return [
        DummyModel, # type: ignore
    ]
