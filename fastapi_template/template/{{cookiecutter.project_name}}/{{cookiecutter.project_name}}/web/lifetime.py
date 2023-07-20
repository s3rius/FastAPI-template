import logging
from typing import Awaitable, Callable

from fastapi import FastAPI
from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.prometheus_enabled == "True" %}
from prometheus_fastapi_instrumentator.instrumentation import \
    PrometheusFastApiInstrumentator

{%- endif %}

{%- if cookiecutter.enable_redis == "True" %}
from {{cookiecutter.project_name}}.services.redis.lifetime import (init_redis,
                                                                   shutdown_redis)

{%- endif %}

{%- if cookiecutter.enable_rmq == "True" %}
from {{cookiecutter.project_name}}.services.rabbit.lifetime import (init_rabbit,
                                                                    shutdown_rabbit)

{%- endif %}

{%- if cookiecutter.enable_kafka == "True" %}
from {{cookiecutter.project_name}}.services.kafka.lifetime import (init_kafka,
                                                                   shutdown_kafka)

{%- endif %}

{%- if cookiecutter.enable_taskiq == "True" %}
from {{cookiecutter.project_name}}.tkq import broker

{%- endif %}


{%- if cookiecutter.orm == "ormar" %}
from {{cookiecutter.project_name}}.db.config import database

{%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations != "True" %}
from sqlalchemy.engine import create_engine
from {{cookiecutter.project_name}}.db.meta import meta
from {{cookiecutter.project_name}}.db.models import load_all_models

{%- endif %}
{%- endif %}

{%- if cookiecutter.otlp_enabled == "True" %}
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import (DEPLOYMENT_ENVIRONMENT, SERVICE_NAME,
                                         TELEMETRY_SDK_LANGUAGE, Resource)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

{%- if cookiecutter.enable_redis == "True" %}
from opentelemetry.instrumentation.redis import RedisInstrumentor

{%- endif %}
{%- if cookiecutter.db_info.name == "postgresql" and cookiecutter.orm in ["ormar", "tortoise"] %}
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor

{%- endif %}
{%- if cookiecutter.orm == "sqlalchemy" %}
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

{%- endif %}
{%- if cookiecutter.enable_rmq == "True" %}
from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor

{%- endif %}
{%- if cookiecutter.enable_loguru != "True" %}
from opentelemetry.instrumentation.logging import LoggingInstrumentor

{%- endif %}
{%- endif %}

{%- if cookiecutter.orm == "psycopg" %}
import psycopg_pool


async def _setup_db(app: FastAPI) -> None:
    """
    Creates connection pool for timescaledb.

    :param app: current FastAPI app.
    """
    app.state.db_pool = psycopg_pool.AsyncConnectionPool(conninfo=str(settings.db_url))
    await app.state.db_pool.wait()
{%- endif %}

{%- if cookiecutter.orm == "sqlalchemy" %}
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

{%- if cookiecutter.enable_migrations != "True" %}
from {{cookiecutter.project_name}}.db.meta import meta
from {{cookiecutter.project_name}}.db.models import load_all_models

{%- endif %}


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
{%- endif %}

{%- if cookiecutter.enable_migrations != "True" %}
{%- if cookiecutter.orm in ["ormar", "sqlalchemy"] %}
async def _create_tables() -> None:  # pragma: no cover
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

{%- if cookiecutter.otlp_enabled == "True" %}
def setup_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    tracer_provider = TracerProvider(
        resource=Resource(
            attributes={
                SERVICE_NAME: "{{cookiecutter.project_name}}",
                TELEMETRY_SDK_LANGUAGE: "python",
                DEPLOYMENT_ENVIRONMENT: settings.environment,
            }
        )
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=settings.opentelemetry_endpoint,
                insecure=True,
            )
        )
    )

    excluded_endpoints = [
        app.url_path_for('health_check'),
        app.url_path_for('openapi'),
        app.url_path_for('swagger_ui_html'),
        app.url_path_for('swagger_ui_redirect'),
        app.url_path_for('redoc_html'),
        {%- if cookiecutter.prometheus_enabled == "True" %}
        "/metrics",
        {%- endif %}
    ]

    FastAPIInstrumentor().instrument_app(
        app,
        tracer_provider=tracer_provider,
        excluded_urls=",".join(excluded_endpoints),
    )
    {%- if cookiecutter.enable_redis == "True" %}
    RedisInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
    {%- endif %}
    {%- if cookiecutter.db_info.name == "postgresql" and cookiecutter.orm in ["ormar", "tortoise"] %}
    AsyncPGInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
    {%- endif %}
    {%- if cookiecutter.orm == "sqlalchemy" %}
    SQLAlchemyInstrumentor().instrument(
        tracer_provider=tracer_provider,
        engine=app.state.db_engine.sync_engine,
    )
    {%- endif %}
    {%- if cookiecutter.enable_rmq == "True" %}
    AioPikaInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
    {%- endif %}
    {%- if cookiecutter.enable_loguru != "True" %}
    LoggingInstrumentor().instrument(
        tracer_provider=tracer_provider,
        set_logging_format=True,
        log_level=logging.getLevelName(settings.log_level.value),
    )
    {%- endif %}

    set_tracer_provider(tracer_provider=tracer_provider)


def stop_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Disables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    FastAPIInstrumentor().uninstrument_app(app)
    {%- if cookiecutter.enable_redis == "True" %}
    RedisInstrumentor().uninstrument()
    {%- endif %}
    {%- if cookiecutter.db_info.name == "postgresql" and cookiecutter.orm in ["ormar", "tortoise"] %}
    AsyncPGInstrumentor().uninstrument()
    {%- endif %}
    {%- if cookiecutter.orm == "sqlalchemy" %}
    SQLAlchemyInstrumentor().uninstrument()
    {%- endif %}
    {%- if cookiecutter.enable_rmq == "True" %}
    AioPikaInstrumentor().uninstrument()
    {%- endif %}

{%- endif %}

{%- if cookiecutter.prometheus_enabled == "True" %}
def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        app,
    ).expose(app, should_gzip=True, name="prometheus_metrics")
{%- endif %}


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        {%- if cookiecutter.enable_taskiq == "True" %}
        if not broker.is_worker_process:
            await broker.startup()
        {%- endif %}
        {%- if cookiecutter.orm == "sqlalchemy" %}
        _setup_db(app)
        {%- elif cookiecutter.orm == "ormar" %}
        await database.connect()
        {%- elif cookiecutter.orm == "psycopg" %}
        await _setup_db(app)
        {%- endif %}
        {%- if cookiecutter.db_info.name != "none" and cookiecutter.enable_migrations != "True" %}
        {%- if cookiecutter.orm in ["ormar", "sqlalchemy"] %}
        await _create_tables()
        {%- endif %}
        {%- endif %}
        {%- if cookiecutter.otlp_enabled == "True" %}
        setup_opentelemetry(app)
        {%- endif %}
        {%- if cookiecutter.enable_redis == "True" %}
        init_redis(app)
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        init_rabbit(app)
        {%- endif %}
        {%- if cookiecutter.enable_kafka == "True" %}
        await init_kafka(app)
        {%- endif %}
        {%- if cookiecutter.prometheus_enabled == "True" %}
        setup_prometheus(app)
        {%- endif %}
        app.middleware_stack = app.build_middleware_stack()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        {%- if cookiecutter.enable_taskiq == "True" %}
        if not broker.is_worker_process:
            await broker.shutdown()
        {%- endif %}
        {%- if cookiecutter.orm == "sqlalchemy" %}
        await app.state.db_engine.dispose()
        {% elif cookiecutter.orm == "ormar" %}
        await database.disconnect()
        {%- elif cookiecutter.orm == "psycopg" %}
        await app.state.db_pool.close()
        {%- endif %}
        {%- if cookiecutter.enable_redis == "True" %}
        await shutdown_redis(app)
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        await shutdown_rabbit(app)
        {%- endif %}
        {%- if cookiecutter.enable_kafka == "True" %}
        await shutdown_kafka(app)
        {%- endif %}
        {%- if cookiecutter.otlp_enabled == "True" %}
        stop_opentelemetry(app)
        {%- endif %}
        pass  # noqa: WPS420

    return _shutdown
