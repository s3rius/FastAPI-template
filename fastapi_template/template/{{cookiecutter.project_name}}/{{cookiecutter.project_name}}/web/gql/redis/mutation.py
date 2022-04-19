import strawberry
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
        Set value in redis.

        :param data: key and value to insert.
        :param info: connection info.
        :return: key and value.
        """
        await info.context.redis.set(name=data.key, value=data.value)
        return RedisDTO(key=data.key, value=data.value)  # type: ignore
