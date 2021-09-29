import os
from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from {{cookiecutter.project_name}}.settings import settings

{% if cookiecutter.db_info.name == "postgresql" -%}
async def create_database() -> None:
    """Create a databse."""
    db_url = make_url(str(settings.db_url.with_path('/postgres')))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'",  # noqa: E501, S608
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            )
        )

async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path('/postgres')))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
        "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
        "FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
        "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.db_base}"'))


{%- endif %}
{%- if cookiecutter.db_info.name == "mysql" %}
async def create_database() -> None:
    """Create a databse."""
    engine = create_async_engine(str(settings.db_url.with_path("/mysql")))

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                f" WHERE SCHEMA_NAME='{settings.db_base}';",
            )
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE {settings.db_base};'
            )
        )

async def drop_database() -> None:
    """Drop current database."""
    engine = create_async_engine(str(settings.db_url.with_path("/mysql")))
    async with engine.connect() as conn:
        await conn.execute(text(f'DROP DATABASE {settings.db_base};'))
{%- endif %}
{%- if cookiecutter.db_info.name == "sqlite" %}
async def create_database() -> None:
    """Create a databse."""

async def drop_database() -> None:
    """Drop current database."""
    if settings.db_file.exists():
        os.remove(settings.db_file)

{%- endif %}
