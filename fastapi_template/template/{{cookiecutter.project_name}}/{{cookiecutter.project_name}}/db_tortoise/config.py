from typing import List

from {{cookiecutter.project_name}}.settings import settings

MODELS_MODULES: List[str] = [{%- if cookiecutter.add_dummy == 'True' %}"{{cookiecutter.project_name}}.db.models.dummy_model"{%- endif %}]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES {%- if cookiecutter.enable_migrations == "True" %} + ["aerich.models"] {%- endif %} ,
            "default_connection": "default",
        },
    },
}
