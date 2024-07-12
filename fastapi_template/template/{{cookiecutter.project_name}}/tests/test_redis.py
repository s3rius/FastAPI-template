import uuid

import fakeredis
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import ConnectionPool, Redis
from starlette import status


@pytest.mark.anyio
async def test_setting_value(
    fastapi_app: FastAPI,
    fake_redis_pool: ConnectionPool,
    client: AsyncClient,
) -> None:
    """
    Tests that you can set value in redis.

    :param fastapi_app: current application fixture.
    :param fake_redis_pool: fake redis pool.
    :param client: client fixture.
    """
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('set_redis_value')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    {%- endif %}

    test_key = uuid.uuid4().hex
    test_val = uuid.uuid4().hex
    {%- if cookiecutter.api_type == 'rest' %}
    response = await client.put(url, json={
        "key": test_key,
        "value": test_val
    })
    {%- elif cookiecutter.api_type == 'graphql' %}
    query = """
    mutation ($key: String!, $val: String!) {
        setRedisValue(data: { key: $key, value: $val }) {
            key
            value
        }
    }
    """
    response = await client.post(
        url,
        json={
            "query": query,
            "variables": {"key": test_key, "val": test_val},
        },
    )
    {%- endif %}

    assert response.status_code == status.HTTP_200_OK
    async with Redis(connection_pool=fake_redis_pool) as redis:
        actual_value = await redis.get(test_key)
    assert actual_value.decode() == test_val


@pytest.mark.anyio
async def test_getting_value(
    fastapi_app: FastAPI,
    fake_redis_pool: ConnectionPool,
    client: AsyncClient,
) -> None:
    """
    Tests that you can get value from redis by key.

    :param fastapi_app: current application fixture.
    :param fake_redis_pool: fake redis pool.
    :param client: client fixture.
    """
    test_key = uuid.uuid4().hex
    test_val = uuid.uuid4().hex
    async with Redis(connection_pool=fake_redis_pool) as redis:
        await redis.set(test_key, test_val)

    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('get_redis_value')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_post')
    {%- endif %}

    {%- if cookiecutter.api_type == 'rest' %}
    response = await client.get(url, params={"key": test_key})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['key'] == test_key
    assert response.json()['value'] == test_val
    {%- elif cookiecutter.api_type == 'graphql' %}
    response = await client.post(
        url,
        json={
            "query": "query($key:String!){redis:getRedisValue(key:$key){key value}}",
            "variables": {
                "key": test_key,
            },
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["redis"]["key"] == test_key
    assert response.json()["data"]["redis"]["value"] == test_val
    {%- endif %}

