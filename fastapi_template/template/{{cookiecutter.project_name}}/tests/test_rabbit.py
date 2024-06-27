import uuid

import pytest
from aio_pika import Channel
from aio_pika.abc import AbstractQueue
from aio_pika.exceptions import QueueEmpty
from aio_pika.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_message_publishing(
    fastapi_app: FastAPI,
    client: AsyncClient,
    test_queue: AbstractQueue,
    test_exchange_name: str,
    test_routing_key: str,
) -> None:
    """
    Tests that message is published correctly.

    It sends message to rabbitmq and reads it
    from binded queue.
    """
    message_text = uuid.uuid4().hex
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for("send_rabbit_message")
    await client.post(
        url,
        json={
            "exchange_name": test_exchange_name,
            "routing_key": test_routing_key,
            "message": message_text,
        },
    )
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    await client.post(
        url,
        json={
            "query": "mutation($message:RabbitMessageDTO!)"
                     "{sendRabbitMessage(message:$message)}",
            "variables": {
                "message": {
                    "exchangeName": test_exchange_name,
                    "routingKey": test_routing_key,
                    "message": message_text,
                },
            },
        },
    )
    {%- endif %}
    message = await test_queue.get(timeout=1)
    assert message is not None
    await message.ack()
    assert message.body.decode("utf-8") == message_text


@pytest.mark.anyio
async def test_message_wrong_exchange(
    fastapi_app: FastAPI,
    client: AsyncClient,
    test_queue: AbstractQueue,
    test_exchange_name: str,
    test_routing_key: str,
    test_rmq_pool: Pool[Channel],
) -> None:
    """
    Tests that message can be published in undeclared exchange.

    It sends message to random queue,
    tries to get message from binded queue
    and checks that new exchange were created.
    """
    random_exchange = uuid.uuid4().hex
    assert random_exchange != test_exchange_name
    message_text = uuid.uuid4().hex
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for("send_rabbit_message")
    await client.post(
        url,
        json={
            "exchange_name": random_exchange,
            "routing_key": test_routing_key,
            "message": message_text,
        },
    )
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    await client.post(
        url,
        json={
            "query": "mutation($message:RabbitMessageDTO!)"
                     "{sendRabbitMessage(message:$message)}",
            "variables": {
                "message": {
                    "exchangeName": random_exchange,
                    "routingKey": test_routing_key,
                    "message": message_text,
                },
            },
        },
    )
    {%- endif %}
    with pytest.raises(QueueEmpty):
        await test_queue.get(timeout=1)

    async with test_rmq_pool.acquire() as conn:
        exchange = await conn.get_exchange(random_exchange, ensure=True)
        await exchange.delete(if_unused=False)
