from piccolo.conf.apps import AppRegistry
from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.db_info.name == "postgresql" %}
from piccolo.engine.postgres import PostgresEngine

DB = PostgresEngine(
    config={
        "database": settings.db_base,
        "user": settings.db_user,
        "password": settings.db_pass,
        "host": settings.db_host,
        "port": settings.db_port,
    }
)



{%- elif cookiecutter.db_info.name == "sqlite" %}
from piccolo.engine.sqlite import SQLiteEngine

DB = SQLiteEngine(path=str(settings.db_file))
{%- endif %}


APP_REGISTRY = AppRegistry(
    apps=["{{cookiecutter.project_name}}.db.app_conf"]
)
