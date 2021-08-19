from aioredis import Redis
from fastapi import APIRouter
from fastapi.param_functions import Depends

from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_connection
from {{cookiecutter.project_name}}.web.api.redis.schema import RedisValueDTO

router = APIRouter()


@router.get("/", response_model=RedisValueDTO)
async def get_value(
    key: str,
    redis: Redis = Depends(get_redis_connection),
) -> RedisValueDTO:
    """
    Get value from redis.

    :param key: redis key, to get data from.
    :param redis: redis connection.
    :returns: information from redis.
    """
    redis_value = await redis.get(key)
    return RedisValueDTO(
        key=key,
        value=redis_value,
    )


@router.put("/")
async def set_value(
    redis_value: RedisValueDTO,
    redis: Redis = Depends(get_redis_connection),
) -> None:
    """
    Set value in redis.

    :param redis_value: new value data.
    :param redis: redis connection.
    """
    await redis.set(name=redis_value.key, value=redis_value.value)
