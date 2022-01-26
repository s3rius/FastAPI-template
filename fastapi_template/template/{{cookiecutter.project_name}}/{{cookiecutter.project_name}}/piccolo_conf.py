from piccolo.conf.apps import AppRegistry

from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.db_info.name == "postgresql" %}
from piccolo.engine.postgres import PostgresEngine

DB = PostgresEngine(config={'host': settings.db_host,
                            'port': settings.db_port,
                            'user': settings.db_user,
                            'password': settings.db_pass,
                            'database': settings.db_base})

{%- elif cookiecutter.db_info.name == "sqlite" %}
from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine(path=settings.db_file)
{%- endif %}

# A list of paths to piccolo apps
# e.g. ['sample_project.db_piccolo.dao.piccolo_app']
{%- if cookiecutter.add_dummy == True %}
APP_REGISTRY = AppRegistry(
    apps=['{{cookiecutter.project_name}}.db_piccolo.dao.piccolo_app']
)

{%- else %}

APP_REGISTRY = AppRegistry(
    apps=[]
)
{%- endif %}
