import sys
from typing import Any, Callable

import alembic.config
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from src.api import api_router
{% if cookiecutter.pg_driver == "aiopg" -%}
from src.services.db import db_engine
{% else %}
from src.services.db import db_url
from asyncpgsa import pg
{% endif %}
{% if cookiecutter.add_redis == "True" -%}
from src.services.redis import redis
{% endif %}
from src.settings import Settings, settings

logger.configure(
    handlers=[{
        "sink": sys.stderr,
        "backtrace": False,
        "diagnose": settings.is_dev,
        "catch": False,
        "colorize": settings.is_dev,
    }]
)

app = FastAPI(
    title="{{cookiecutter.project_name}}",
    description="{{cookiecutter.project_description}}",
)

app.include_router(prefix="", router=api_router)


@app.on_event("startup")
async def startup() -> None:
    {% if cookiecutter.add_redis == "True" -%}
    await redis.create_pool()
    {% endif %}
    {% if cookiecutter.pg_driver == "aiopg" -%}
    await db_engine.connect()
    {% else %}
    await pg.init(str(db_url))
    {% endif %}


@app.on_event("shutdown")
async def shutdown() -> None:
    {% if cookiecutter.add_redis == "True" -%}
    await redis.shutdown()
    {% endif %}
    {% if cookiecutter.pg_driver == "aiopg" -%}
    await db_engine.close()
    {% else %}
    await pg.pool.close()
    {% endif %}



@app.middleware("http")
async def exception_logger(request: Request, call_next: Callable[..., Any]) -> Any:
    """
    Just to log all exception with godlike logger from loguru.
    """
    target_func = logger.catch()(call_next)
    response = await target_func(request)
    return response


if settings.is_dev:
    alembic.config.main(
        [
            "--raiseerr",
            "upgrade",
            "head",
        ]
    )

    @app.get("/conf")
    def reveal_current_configuration() -> Settings:
        """
        Show current application settings
        ## Available only under development
        """
        return settings