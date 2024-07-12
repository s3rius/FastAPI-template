import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_echo(fastapi_app: FastAPI, client: AsyncClient) -> None:
    """
    Tests that echo route works.

    :param fastapi_app: current application.
    :param client: client for the app.
    """
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('send_echo_message')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    {%- endif %}
    message = uuid.uuid4().hex
    {%- if cookiecutter.api_type == 'rest' %}
    response = await client.post(url, json={
        "message": message
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == message
    {%- elif cookiecutter.api_type == 'graphql' %}
    response = await client.post(
        url,
        json={
            "query": "query($message: String!){echo(message: $message)}",
            "variables": {
                "message": message,
            },
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['echo'] == message
    {%- endif %}

