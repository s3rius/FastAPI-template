import asyncio
import uuid

import pytest
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from {{cookiecutter.project_name}}.settings import settings


@pytest.mark.anyio
async def test_message_publishing(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test that messages are published correctly.

    It sends message to kafka, reads it and
    validates that received message has the same
    value.

    :param fastapi_app: current application.
    :param client: httpx client.
    """
    topic_name = uuid.uuid4().hex
    message = uuid.uuid4().hex
    consumer = AIOKafkaConsumer(
        topic_name,
        bootstrap_servers=settings.kafka_bootstrap_servers,
    )
    await consumer.start()

    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for("send_kafka_message")
    response = await client.post(
        url,
        json={
            "topic": topic_name,
            "message": message,
        },
    )
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    response = await client.post(
        url,
        json={
            "query": "mutation($message:KafkaMessageDTO!)"
                     "{sendKafkaMessage(message:$message)}",
            "variables": {
                "message": {
                    "topic": topic_name,
                    "message": message,
                },
            },
        },
    )
    {%- endif %}


    assert response.status_code == status.HTTP_200_OK

    msg = await asyncio.wait_for(consumer.getone(), timeout=1)
    assert msg.value == message.encode()
