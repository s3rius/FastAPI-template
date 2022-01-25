import os
from piccolo.conf.apps import table_finder

from piccolo.conf.apps import AppConfig

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name='dao',
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, 'migrations'),
    table_classes=table_finder(
        modules=['{{cookiecutter.project_name}}.db_piccolo.dao.tables']
    ),
    migration_dependencies=[],
    commands=[]
)
