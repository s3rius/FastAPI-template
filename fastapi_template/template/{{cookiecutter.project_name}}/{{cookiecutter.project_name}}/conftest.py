import asyncio
from asyncio.events import AbstractEventLoop
import sys
from typing import Any, Generator, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
{%- if cookiecutter.enable_redis == "True" %}
from fakeredis.aioredis import FakeRedis
from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_connection
{%- endif %}

from {{cookiecutter.project_name}}.settings import settings
from {{cookiecutter.project_name}}.web.application import get_app


{%- if cookiecutter.orm == "sqlalchemy" %}
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.orm import sessionmaker
from {{cookiecutter.project_name}}.db.dependencies import get_db_session
from {{cookiecutter.project_name}}.db.utils import create_database, drop_database
{%- elif cookiecutter.orm == "tortoise" %}
from tortoise.contrib.test import finalizer, initializer
from tortoise import Tortoise
from {{cookiecutter.project_name}}.db.config import MODELS_MODULES, TORTOISE_CONFIG
import nest_asyncio

nest_asyncio.apply()
{%- elif cookiecutter.orm == "ormar" %}
from sqlalchemy.engine import create_engine
from {{cookiecutter.project_name}}.db.config import database
from {{cookiecutter.project_name}}.db.utils import create_database, drop_database
{%- endif %}


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return 'asyncio'

{%- if cookiecutter.orm == "sqlalchemy" %}
@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from {{cookiecutter.project_name}}.db.meta import meta  # noqa: WPS433
    from {{cookiecutter.project_name}}.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()

@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()

{%- elif cookiecutter.orm == "tortoise" %}

@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Initialize models and database.

    :yields: Nothing.
    """
    initializer(
        MODELS_MODULES,
        db_url=str(settings.db_url),
        app_label="models",
    )
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await Tortoise.close_connections()
    finalizer()

{%- elif cookiecutter.orm == "ormar" %}

@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Create models and databases.

    :yield: new engine.
    """
    from {{cookiecutter.project_name}}.db.meta import meta  # noqa: WPS433
    from {{cookiecutter.project_name}}.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    create_database()

    engine = create_engine(str(settings.db_url))
    with engine.begin() as conn:
        meta.create_all(conn)

    engine.dispose()

    await database.connect()

    yield

    await database.disconnect()
    drop_database()

{%- endif %}


{% if cookiecutter.enable_redis == "True" -%}
@pytest.fixture
async def fake_redis() -> AsyncGenerator[FakeRedis, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    redis = FakeRedis(decode_responses=True)
    yield redis
    await redis.close()

{%- endif %}

@pytest.fixture
def fastapi_app(
    {%- if cookiecutter.orm == "sqlalchemy" %}
    dbsession: AsyncSession,
    {%- endif %}
    {% if cookiecutter.enable_redis == "True" -%}
    fake_redis: FakeRedis,
    {%- endif %}
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    {% if cookiecutter.orm == "sqlalchemy" -%}
    application.dependency_overrides[get_db_session] = lambda: dbsession
    {%- endif %}
    {%- if cookiecutter.enable_redis == "True" %}
    application.dependency_overrides[get_redis_connection] = lambda: fake_redis
    {%- endif %}

    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
            yield ac
