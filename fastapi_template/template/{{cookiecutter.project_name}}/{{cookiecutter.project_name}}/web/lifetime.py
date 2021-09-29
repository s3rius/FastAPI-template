from typing import Awaitable, Callable

from fastapi import FastAPI

from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.enable_redis == "True" %}
import aioredis
{%- endif %}

{%- if cookiecutter.db_info.name != "none" and cookiecutter.orm == "sqlalchemy" %}
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


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
    app.state.redis_pool = aioredis.ConnectionPool.from_url(
        str(settings.redis_url),
    )
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
        {%- if cookiecutter.db_info.name != "none" and cookiecutter.orm == "sqlalchemy" %}
        _setup_db(app)
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
        {%- if cookiecutter.db_info.name != "none" and cookiecutter.orm == "sqlalchemy" %}
        await app.state.db_engine.dispose()
        {%- endif %}
        {%- if cookiecutter.enable_redis == "True" %}
        await app.state.redis_pool.disconnect()
        {%- endif %}
        pass  # noqa: WPS420

    return _shutdown
