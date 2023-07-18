from fastapi import APIRouter
from fastapi.param_functions import Depends
from redis.asyncio import ConnectionPool, Redis
from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_pool
from {{cookiecutter.project_name}}.web.api.redis.schema import RedisValueDTO

router = APIRouter()


@router.get("/", response_model=RedisValueDTO)
async def get_redis_value(
    key: str,
    redis_pool: ConnectionPool = Depends(get_redis_pool),
) -> RedisValueDTO:
    """
    Get value from redis.

    :param key: redis key, to get data from.
    :param redis_pool: redis connection pool.
    :returns: information from redis.
    """
    async with Redis(connection_pool=redis_pool) as redis:
        redis_value = await redis.get(key)
    return RedisValueDTO(
        key=key,
        value=redis_value,
    )


@router.put("/")
async def set_redis_value(
    redis_value: RedisValueDTO,
    redis_pool: ConnectionPool = Depends(get_redis_pool),
) -> None:
    """
    Set value in redis.

    :param redis_value: new value data.
    :param redis_pool: redis connection pool.
    """
    if redis_value.value is not None:
        async with Redis(connection_pool=redis_pool) as redis:
            await redis.set(name=redis_value.key, value=redis_value.value)
