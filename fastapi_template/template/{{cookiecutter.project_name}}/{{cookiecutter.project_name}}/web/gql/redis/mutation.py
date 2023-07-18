import strawberry
from redis.asyncio import Redis
from strawberry.types import Info
from {{cookiecutter.project_name}}.web.gql.context import Context
from {{cookiecutter.project_name}}.web.gql.redis.schema import RedisDTO, RedisDTOInput


@strawberry.type
class Mutation:
    """Mutations for redis."""

    @strawberry.mutation(description="Set value in redis")
    async def set_redis_value(
        self,
        data: RedisDTOInput,
        info: Info[Context, None],
    ) -> RedisDTO:
        """
        Sets value in redis.

        :param data: key and value to insert.
        :param info: connection info.
        :return: key and value.
        """
        async with Redis(connection_pool=info.context.redis_pool) as redis:
            await redis.set(name=data.key, value=data.value)
        return RedisDTO(key=data.key, value=data.value)  # type: ignore
