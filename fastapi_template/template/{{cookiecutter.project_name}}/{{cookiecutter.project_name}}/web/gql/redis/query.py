import strawberry
from redis.asyncio import Redis
from strawberry.types import Info
from {{cookiecutter.project_name}}.web.gql.context import Context
from {{cookiecutter.project_name}}.web.gql.redis.schema import RedisDTO


@strawberry.type
class Query:
    """Query to interact with redis."""

    @strawberry.field(description="Get value from redis")
    async def get_redis_value(self, key: str, info: Info[Context, None]) -> RedisDTO:
        """
        Gets value from redis.

        :param key: key to search for.
        :param info: resolver context.
        :return: information from redis.
        """
        async with Redis(connection_pool=info.context.redis_pool) as redis:
            val = await redis.get(name=key)
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        return RedisDTO(key=key, value=val)  # type: ignore
