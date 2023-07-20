import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from {{cookiecutter.project_name}}.settings import settings
from {{cookiecutter.project_name}}.web.api.router import api_router

{%- if cookiecutter.api_type == 'graphql' %}
from {{cookiecutter.project_name}}.web.gql.router import gql_router

{%- endif %}
from importlib import metadata

from {{cookiecutter.project_name}}.web.lifetime import (register_shutdown_event,
                                                        register_startup_event)

{%- if cookiecutter.orm == 'tortoise' %}
from tortoise.contrib.fastapi import register_tortoise
from {{cookiecutter.project_name}}.db.config import TORTOISE_CONFIG

{%- endif %}

{%- if cookiecutter.sentry_enabled == "True" %}
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

{%- if cookiecutter.orm == "sqlalchemy" %}
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

{%- endif %}
{%- endif %}

{%- if cookiecutter.enable_loguru == "True" %}
from {{cookiecutter.project_name}}.logging import configure_logging

{%- endif %}

{%- if cookiecutter.self_hosted_swagger == 'True' %}
from pathlib import Path

from fastapi.staticfiles import StaticFiles

APP_ROOT = Path(__file__).parent.parent
{%- endif %}


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    {%- if cookiecutter.enable_loguru == "True" %}
    configure_logging()
    {%- endif %}
    {%- if cookiecutter.sentry_enabled == "True" %}
    if settings.sentry_dsn:
        # Enables sentry integration.
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=settings.sentry_sample_rate,
            environment=settings.environment,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                LoggingIntegration(
                    level=logging.getLevelName(
                        settings.log_level.value,
                    ),
                    event_level=logging.ERROR,
                ),
                {%- if cookiecutter.orm == "sqlalchemy" %}
                SqlalchemyIntegration(),
                {%- endif %}
            ],
        )
    {%- endif %}
    app = FastAPI(
        title="{{cookiecutter.project_name}}",
        version=metadata.version("{{cookiecutter.project_name}}"),
        {%- if cookiecutter.self_hosted_swagger == 'True' %}
        docs_url=None,
        redoc_url=None,
        {% else %}
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        {%- endif %}
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    {%- if cookiecutter.api_type == 'graphql' %}
    # Graphql router
    app.include_router(router=gql_router, prefix="/graphql")
    {%- endif %}

    {%- if cookiecutter.self_hosted_swagger == 'True' %}
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static"
    )
    {% endif %}

    {%- if cookiecutter.orm == 'tortoise' %}
    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
        {%- if cookiecutter.enable_migrations != "True" %}
        generate_schemas=True,
        {%- endif %}
    )
    {%- endif %}

    return app
