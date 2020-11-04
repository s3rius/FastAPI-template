import sys
from typing import Any, Callable

import alembic.config
from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request
from starlette.responses import UJSONResponse

from src.api import api_router
from src.services.db import db_engine
{% if cookiecutter.add_redis == "True" -%}
from src.services.redis import redis
{% endif %}
from src.settings import settings

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
    default_response_class=UJSONResponse
)

app.include_router(prefix="", router=api_router)


@app.on_event("startup")
async def startup() -> None:
    {% if cookiecutter.add_redis == "True" -%}
    await redis.create_pool()
    {% endif %}
    await db_engine.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    {% if cookiecutter.add_redis == "True" -%}
    await redis.shutdown()
    {% endif %}
    await db_engine.close()



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
