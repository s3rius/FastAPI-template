import os

from sqlalchemy import text
from sqlalchemy.engine import URL, create_engine, make_url
from {{cookiecutter.project_name}}.settings import settings

{% if cookiecutter.db_info.name == "postgresql" -%}
def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(settings.db_url.with_path('/postgres')))
    engine = create_engine(db_url, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        database_existance = conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'",  # noqa: E501, S608
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        drop_database()

    with engine.connect() as conn:  # noqa: WPS440
        conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            )
        )

def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path('/postgres')))
    engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        disc_users = (
        "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
        "FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
        "AND pid <> pg_backend_pid();"
        )
        conn.execute(text(disc_users))
        conn.execute(text(f'DROP DATABASE "{settings.db_base}"'))


{%- endif %}
{%- if cookiecutter.db_info.name == "mysql" %}
def create_database() -> None:
    """Create a database."""
    engine = create_engine(str(settings.db_url.with_path("/mysql")))

    with engine.connect() as conn:
        database_existance = conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                f" WHERE SCHEMA_NAME='{settings.db_base}';",
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        drop_database()

    with engine.connect() as conn:  # noqa: WPS440
        conn.execute(
            text(
                f'CREATE DATABASE {settings.db_base};'
            )
        )

def drop_database() -> None:
    """Drop current database."""
    engine = create_engine(str(settings.db_url.with_path("/mysql")))
    with engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE {settings.db_base};'))
{%- endif %}
{%- if cookiecutter.db_info.name == "sqlite" %}
def create_database() -> None:
    """Create a database."""

def drop_database() -> None:
    """Drop current database."""
    if settings.db_file.exists():
        os.remove(settings.db_file)

{%- endif %}
