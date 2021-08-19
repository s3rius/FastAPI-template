from typing import AsyncGenerator

from aioredis import Redis
from starlette.requests import Request


async def get_redis_connection(request: Request) -> AsyncGenerator[Redis, None]:
    """
    Get redis client.

    This dependency aquires connection from pool.

    :param request: current request.
    :yield:  redis client.
    """
    redis_client = Redis(connection_pool=request.app.state.redis_pool)

    yield redis_client

    await redis_client.close()
