import asyncio
import sys
import uuid
from asyncio.events import AbstractEventLoop
from typing import Any, AsyncGenerator, Generator
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

{%- if cookiecutter.enable_redis == "True" %}
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from redis.asyncio import ConnectionPool
from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_pool

{%- endif %}
{%- if cookiecutter.enable_rmq == "True" %}
from aio_pika import Channel
from aio_pika.abc import AbstractExchange, AbstractQueue
from aio_pika.pool import Pool
from {{cookiecutter.project_name}}.services.rabbit.dependencies import \
    get_rmq_channel_pool
from {{cookiecutter.project_name}}.services.rabbit.lifetime import (init_rabbit,
                                                                    shutdown_rabbit)

{%- endif %}
{%- if cookiecutter.enable_kafka == "True" %}
from aiokafka import AIOKafkaProducer
from {{cookiecutter.project_name}}.services.kafka.dependencies import get_kafka_producer
from {{cookiecutter.project_name}}.services.kafka.lifetime import (init_kafka,
                                                                   shutdown_kafka)

{%- endif %}

from {{cookiecutter.project_name}}.settings import settings
from {{cookiecutter.project_name}}.web.application import get_app

{%- if cookiecutter.orm == "sqlalchemy" %}
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from {{cookiecutter.project_name}}.db.dependencies import get_db_session
from {{cookiecutter.project_name}}.db.utils import create_database, drop_database

{%- elif cookiecutter.orm == "tortoise" %}
import nest_asyncio
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer
from {{cookiecutter.project_name}}.db.config import MODELS_MODULES, TORTOISE_CONFIG

nest_asyncio.apply()
{%- elif cookiecutter.orm == "ormar" %}
from sqlalchemy.engine import create_engine
from {{cookiecutter.project_name}}.db.config import database
from {{cookiecutter.project_name}}.db.utils import create_database, drop_database

{%- elif cookiecutter.orm == "psycopg" %}
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool
from {{cookiecutter.project_name}}.db.dependencies import get_db_pool

{%- elif cookiecutter.orm == "piccolo" %}
{%- if cookiecutter.db_info.name == "postgresql" %}
from piccolo.engine.postgres import PostgresEngine

{%- endif %}
from piccolo.conf.apps import Finder
from piccolo.table import create_tables, drop_tables

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

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
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

{%- elif cookiecutter.orm == "psycopg" %}

async def drop_db() -> None:
    """Drops database after tests."""
    pool = AsyncConnectionPool(conninfo=str(settings.db_url.with_path("/postgres")))
    await pool.wait()
    async with pool.connection() as conn:
        await conn.set_autocommit(True)
        await conn.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = %(dbname)s "
            "AND pid <> pg_backend_pid();",
            params={
                "dbname": settings.db_base,
            }
        )
        await conn.execute(
            f"DROP DATABASE {settings.db_base}",
        )
    await pool.close()


async def create_db() -> None:  # noqa: WPS217
    """Creates database for tests."""
    pool = AsyncConnectionPool(conninfo=str(settings.db_url.with_path("/postgres")))
    await pool.wait()
    async with pool.connection() as conn_check:
        res = await conn_check.execute(
            "SELECT 1 FROM pg_database WHERE datname=%(dbname)s",
            params={
                "dbname": settings.db_base,
            }
        )
        db_exists = False
        row = await res.fetchone()
        if row is not None:
            db_exists = row[0]

    if db_exists:
        await drop_db()

    async with pool.connection() as conn_create:
        await conn_create.set_autocommit(True)
        await conn_create.execute(
            f"CREATE DATABASE {settings.db_base};",
        )
    await pool.close()


async def create_tables(connection: AsyncConnection[Any]) -> None:
    """
    Create tables for your database.

    Since psycopg doesn't have migration tool,
    you must create your tables for tests.

    :param connection: connection to database.
    """
    {%- if cookiecutter.add_dummy == 'True' %}
    await connection.execute(
        "CREATE TABLE dummy ("
        "id SERIAL primary key,"
        "name VARCHAR(200)"
        ");"
    )
    {%- endif %}
    pass  # noqa: WPS420


@pytest.fixture
async def dbpool() -> AsyncGenerator[AsyncConnectionPool, None]:
    """
    Creates database connections pool to test database.

    This connection must be used in tests and for application.

    :yield: database connections pool.
    """
    await create_db()
    pool = AsyncConnectionPool(conninfo=str(settings.db_url))
    await pool.wait()

    async with pool.connection() as create_conn:
        await create_tables(create_conn)

    try:
        yield pool
    finally:
        await pool.close()
        await drop_db()

{%- elif cookiecutter.orm == "piccolo" %}

{%- if cookiecutter.db_info.name == "postgresql" %}
async def drop_database(engine: PostgresEngine) -> None:
    """
    Drops test database.

    :param engine: engine connected to postgres database.
    """
    await engine.run_ddl(
        "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
        "FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
        "AND pid <> pg_backend_pid();",
    )
    await engine.run_ddl(
        f"DROP DATABASE {settings.db_base};",
    )
{%- endif %}

@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Fixture to create all tables before test and drop them after.

    :yield: nothing.
    """
    {%- if cookiecutter.db_info.name == "postgresql" %}
    engine = PostgresEngine(
        config={
            "database": "postgres",
            "user": settings.db_user,
            "password": settings.db_pass,
            "host": settings.db_host,
            "port": settings.db_port,
        },
    )
    await engine.start_connection_pool()

    db_exists = await engine.run_ddl(
        f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'"  # noqa: S608
    )
    if db_exists:
        await drop_database(engine)
    await engine.run_ddl(f"CREATE DATABASE {settings.db_base}")
    {%- endif %}
    tables = Finder().get_table_classes()
    create_tables(*tables, if_not_exists=True)

    yield

    drop_tables(*tables)
    {%- if cookiecutter.db_info.name == "postgresql" %}
    await drop_database(engine)
    {%- endif %}

{%- endif %}

{%- if cookiecutter.enable_rmq == 'True' %}

@pytest.fixture
async def test_rmq_pool() -> AsyncGenerator[Channel, None]:
    """
    Create rabbitMQ pool.

    :yield: channel pool.
    """
    app_mock = Mock()
    init_rabbit(app_mock)
    yield app_mock.state.rmq_channel_pool
    await shutdown_rabbit(app_mock)


@pytest.fixture
async def test_exchange_name() -> str:
    """
    Name of an exchange to use in tests.

    :return: name of an exchange.
    """
    return uuid.uuid4().hex


@pytest.fixture
async def test_routing_key() -> str:
    """
    Name of routing key to use while binding test queue.

    :return: key string.
    """
    return uuid.uuid4().hex


@pytest.fixture
async def test_exchange(
    test_exchange_name: str,
    test_rmq_pool: Pool[Channel],
) -> AsyncGenerator[AbstractExchange, None]:
    """
    Creates test exchange.

    :param test_exchange_name: name of an exchange to create.
    :param test_rmq_pool: channel pool for rabbitmq.
    :yield: created exchange.
    """
    async with test_rmq_pool.acquire() as conn:
        exchange = await conn.declare_exchange(
            name=test_exchange_name,
            auto_delete=True,
        )
        yield exchange

        await exchange.delete(if_unused=False)


@pytest.fixture
async def test_queue(
    test_exchange: AbstractExchange,
    test_rmq_pool: Pool[Channel],
    test_routing_key: str,
) -> AsyncGenerator[AbstractQueue, None]:
    """
    Creates queue connected to exchange.

    :param test_exchange: exchange to bind queue to.
    :param test_rmq_pool: channel pool for rabbitmq.
    :param test_routing_key: routing key to use while binding.
    :yield: queue binded to test exchange.
    """
    async with test_rmq_pool.acquire() as conn:
        queue = await conn.declare_queue(name=uuid.uuid4().hex)
        await queue.bind(
            exchange=test_exchange,
            routing_key=test_routing_key,
        )
        yield queue

        await queue.delete(if_unused=False, if_empty=False)

{%- endif %}

{%- if cookiecutter.enable_kafka == "True" %}

@pytest.fixture
async def test_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    """
    Creates kafka's producer.

    :yields: kafka's producer.
    """
    app_mock = Mock()
    await init_kafka(app_mock)
    yield app_mock.state.kafka_producer
    await shutdown_kafka(app_mock)

{%- endif %}

{% if cookiecutter.enable_redis == "True" -%}
@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()

{%- endif %}

@pytest.fixture
def fastapi_app(
    {%- if cookiecutter.orm == "sqlalchemy" %}
    dbsession: AsyncSession,
    {%- elif cookiecutter.orm == "psycopg" %}
    dbpool: AsyncConnectionPool,
    {%- endif %}
    {% if cookiecutter.enable_redis == "True" -%}
    fake_redis_pool: ConnectionPool,
    {%- endif %}
    {%- if cookiecutter.enable_rmq == 'True' %}
    test_rmq_pool: Pool[Channel],
    {%- endif %}
    {%- if cookiecutter.enable_kafka == "True" %}
    test_kafka_producer: AIOKafkaProducer,
    {%- endif %}
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    {%- if cookiecutter.orm == "sqlalchemy" %}
    application.dependency_overrides[get_db_session] = lambda: dbsession
    {%- elif cookiecutter.orm == "psycopg" %}
    application.dependency_overrides[get_db_pool] = lambda: dbpool
    {%- endif %}
    {%- if cookiecutter.enable_redis == "True" %}
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    {%- endif %}
    {%- if cookiecutter.enable_rmq == 'True' %}
    application.dependency_overrides[get_rmq_channel_pool] = lambda: test_rmq_pool
    {%- endif %}
    {%- if cookiecutter.enable_kafka == "True" %}
    application.dependency_overrides[get_kafka_producer] = lambda: test_kafka_producer
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
