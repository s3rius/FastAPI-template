from fastapi import Depends
from strawberry.fastapi import BaseContext

{%- if cookiecutter.enable_redis == "True" %}
from aioredis import Redis
from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_connection
{%- endif %}

{%- if cookiecutter.enable_rmq == "True" %}
from aio_pika.pool import Pool
from aio_pika import Channel
from {{cookiecutter.project_name}}.services.rabbit.dependencies import get_rmq_channel_pool
{%- endif %}


{%- if cookiecutter.db_info.name != 'none' %}
from {{cookiecutter.project_name}}.db.dependencies import get_db_session
{%- endif %}

{%- if cookiecutter.orm == "sqlalchemy" %}
from sqlalchemy.ext.asyncio import AsyncSession
{%- elif cookiecutter.orm == "psycopg" %}
from psycopg import AsyncConnection
{%- endif %}


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        {%- if cookiecutter.enable_redis == "True" %}
        redis: Redis = Depends(get_redis_connection),
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        rabbit: Pool[Channel] = Depends(get_rmq_channel_pool),
        {%- endif %}
        {%- if cookiecutter.orm == "sqlalchemy" %}
        db_connection: AsyncSession = Depends(get_db_session),
        {%- elif cookiecutter.orm == "psycopg" %}
        db_connection: AsyncConnection[Any] = Depends(get_db_session),
        {%- endif %}
    ) -> None:
        {%- if cookiecutter.enable_redis == "True" %}
        self.redis = redis
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        self.rabbit = rabbit
        {%- endif %}
        {%- if cookiecutter.orm in ["sqlalchemy", "psycopg"] %}
        self.db_connection = db_connection
        {%- endif %}
        pass  # noqa: WPS420


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
