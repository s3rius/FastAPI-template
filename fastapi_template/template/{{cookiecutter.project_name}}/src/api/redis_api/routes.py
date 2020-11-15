from fastapi import APIRouter, HTTPException

from src.api.redis_api.schema import RedisSetModel, RedisValueModel
from src.services.redis import redis

router = APIRouter()
URL_PREFIX = "/redis"


@router.put("/set")
async def set_redis_value(
        redis_target: RedisSetModel,
) -> None:
    set_key = await redis.client.set(redis_target.key, redis_target.value, expire=redis_target.expire)
    if not set_key:
        raise HTTPException(
            status_code=400,
            detail="No, you can't",
        )


@router.get("/get", response_model=RedisValueModel)
async def get_redis_value(
        key: str,
) -> RedisValueModel:
    value = await redis.client.get(key, encoding='utf-8')
    if not value:
        raise HTTPException(
            status_code=400,
            detail="I can't get it",
        )
    return RedisValueModel(value=value)
