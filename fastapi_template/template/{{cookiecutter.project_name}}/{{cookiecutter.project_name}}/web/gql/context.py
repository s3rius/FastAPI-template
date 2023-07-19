from fastapi import Depends
from strawberry.fastapi import BaseContext

{%- if cookiecutter.enable_redis == "True" %}
from redis.asyncio import ConnectionPool
from {{cookiecutter.project_name}}.services.redis.dependency import get_redis_pool

{%- endif %}

{%- if cookiecutter.enable_rmq == "True" %}
from aio_pika import Channel
from aio_pika.pool import Pool
from {{cookiecutter.project_name}}.services.rabbit.dependencies import \
    get_rmq_channel_pool

{%- endif %}

{%- if cookiecutter.enable_kafka == "True" %}
from aiokafka import AIOKafkaProducer
from {{cookiecutter.project_name}}.services.kafka.dependencies import get_kafka_producer

{%- endif %}


{%- if cookiecutter.orm == "sqlalchemy" %}
from sqlalchemy.ext.asyncio import AsyncSession
from {{cookiecutter.project_name}}.db.dependencies import get_db_session

{%- elif cookiecutter.orm == "psycopg" %}
from psycopg_pool import AsyncConnectionPool
from {{cookiecutter.project_name}}.db.dependencies import get_db_pool

{%- endif %}


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        {%- if cookiecutter.enable_redis == "True" %}
        redis_pool: ConnectionPool = Depends(get_redis_pool),
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        rabbit: Pool[Channel] = Depends(get_rmq_channel_pool),
        {%- endif %}
        {%- if cookiecutter.orm == "sqlalchemy" %}
        db_connection: AsyncSession = Depends(get_db_session),
        {%- elif cookiecutter.orm == "psycopg" %}
        db_pool: AsyncConnectionPool = Depends(get_db_pool),
        {%- endif %}
        {%- if cookiecutter.enable_kafka == "True" %}
        kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
        {%- endif %}
    ) -> None:
        {%- if cookiecutter.enable_redis == "True" %}
        self.redis_pool = redis_pool
        {%- endif %}
        {%- if cookiecutter.enable_rmq == "True" %}
        self.rabbit = rabbit
        {%- endif %}
        {%- if cookiecutter.orm  == "sqlalchemy" %}
        self.db_connection = db_connection
        {%- endif %}
        {%- if cookiecutter.orm == "psycopg" %}
        self.db_pool = db_pool
        {%- endif %}
        {%- if cookiecutter.enable_kafka == "True" %}
        self.kafka_producer = kafka_producer
        {%- endif %}
        pass  # noqa: WPS420


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
