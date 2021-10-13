from typing import Awaitable, Callable

from fastapi import FastAPI

from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.enable_redis == "True" %}
import aioredis
{%- endif %}

{%- if cookiecutter.orm == "ormar" %}
from {{cookiecutter.project_name}}.db.config import database
{%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations == "False" %}
from sqlalchemy.engine import create_engine
from {{cookiecutter.project_name}}.db.meta import meta
from {{cookiecutter.project_name}}.db.models import load_all_models
{%- endif %}
{%- endif %}

{%- if cookiecutter.orm == "sqlalchemy" %}
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

{%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations == "False" %}
from {{cookiecutter.project_name}}.db.meta import meta
from {{cookiecutter.project_name}}.db.models import load_all_models
{%- endif %}


def _setup_db(app: FastAPI) -> None:
    """
    Create connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
{%- endif %}

{% if cookiecutter.enable_redis == "True" %}
def _setup_redis(app: FastAPI) -> None:
    """
    Initialize redis connection.

    :param app: current FastAPI app.
    """
    app.state.redis_pool = aioredis.ConnectionPool.from_url(
        str(settings.redis_url),
    )
{%- endif %}

{%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations == "False" %}
{%- if cookiecutter.orm in ["ormar", "sqlalchemy"] %}
async def _create_tables() -> None:
    """Populates tables in the database."""
    load_all_models()
    {%- if cookiecutter.orm == "ormar" %}
    engine = create_engine(str(settings.db_url))
    with engine.connect() as connection:
        meta.create_all(connection)
    engine.dispose()
    {%- elif cookiecutter.orm == "sqlalchemy" %}
    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as connection:
        await connection.run_sync(meta.create_all)
    await engine.dispose()
    {%- endif %}
{%- endif %}
{%- endif %}

def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.

    This function use fastAPI app to store data,
    such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    async def _startup() -> None:  # noqa: WPS430
        {%- if cookiecutter.orm == "sqlalchemy" %}
        _setup_db(app)
        {%- elif cookiecutter.orm == "ormar" %}
        await database.connect()
        {%- endif %}
        {%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations == "False" %}
        {%- if cookiecutter.orm in ["ormar", "sqlalchemy"] %}
        await _create_tables()
        {%- endif %}
        {%- endif %}
        {%- if cookiecutter.enable_redis == "True" %}
        _setup_redis(app)
        {%- endif %}
        pass  # noqa: WPS420

    return _startup


def shutdown(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    async def _shutdown() -> None:  # noqa: WPS430
        {%- if cookiecutter.orm == "sqlalchemy" %}
        await app.state.db_engine.dispose()
        {% elif cookiecutter.orm == "ormar" %}
        await database.disconnect()
        {%- endif %}
        {%- if cookiecutter.enable_redis == "True" %}
        await app.state.redis_pool.disconnect()
        {%- endif %}
        pass  # noqa: WPS420

    return _shutdown
