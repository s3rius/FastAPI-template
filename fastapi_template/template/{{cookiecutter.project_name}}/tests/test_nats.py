import asyncio
import uuid

from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from {{cookiecutter.project_name}}.settings import settings
from natsrpy import Nats


async def test_message_publishing(
    fastapi_app: FastAPI,
    client: AsyncClient,
    test_nats: Nats,
) -> None:
    """
    Test that messages are published correctly.

    It sends message to kafka, reads it and
    validates that received message has the same
    value.

    :param fastapi_app: current application.
    :param client: httpx client.
    """
    subject = uuid.uuid4().hex
    payload = uuid.uuid4().hex

    async with test_nats.subscribe(subject) as sub:
        {%- if cookiecutter.api_type == 'rest' %}
        url = fastapi_app.url_path_for("publish_nats_message")
        response = await client.post(
            url,
            json={
                "subject": subject,
                "message": payload,
            },
        )
        {%- elif cookiecutter.api_type == 'graphql' %}
        url = fastapi_app.url_path_for('handle_http_post')
        response = await client.post(
            url,
            json={
                "query": "mutation($message:NatsMessageDTO!)"
                         "{publishNatsMessage(message:$message)}",
                "variables": {
                    "message": {
                        "subject": subject,
                        "message": payload,
                    },
                },
            },
        )
        {%- endif %}
        assert response.status_code == status.HTTP_200_OK
        message = await asyncio.wait_for(anext(sub), 1.0)
        assert message.payload == payload.encode()
