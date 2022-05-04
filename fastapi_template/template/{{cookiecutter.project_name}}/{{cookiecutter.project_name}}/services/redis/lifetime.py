from fastapi import FastAPI
import aioredis
from {{cookiecutter.project_name}}.settings import settings


def init_redis(app: FastAPI) -> None:
    """
    Creates connection pool for redis.

    :param app: current fastapi application.
    """
    app.state.redis_pool = aioredis.ConnectionPool.from_url(
        str(settings.redis_url),
    )


async def shutdown_redis(app: FastAPI) -> None:
    """
    Closes redis connection pool.

    :param app: current FastAPI app.
    """
    await app.state.redis_pool.disconnect()
