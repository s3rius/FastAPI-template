import os

from piccolo.conf.apps import AppConfig, table_finder
from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).parent


APP_CONFIG = AppConfig(
    app_name='{{cookiecutter.project_name}}_db',
    migrations_folder_path=str(CURRENT_DIRECTORY / 'migrations'),
    table_classes=table_finder(modules=[
        {%- if cookiecutter.add_dummy == "True" %}
        "{{cookiecutter.project_name}}.db.models.dummy_model"
        {%- endif %}
    ]),
    migration_dependencies=[],
    commands=[]
)
