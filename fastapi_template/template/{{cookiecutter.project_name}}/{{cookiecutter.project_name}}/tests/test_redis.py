import uuid
import fakeredis
import pytest

from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from fakeredis.aioredis import FakeRedis


@pytest.mark.anyio
async def test_setting_value(
    fastapi_app: FastAPI,
    fake_redis: FakeRedis,
    client: AsyncClient,
) -> None:
    """
    Tests that you can set value in redis.

    :param fastapi_app: current application fixture.
    :param fake_redis: fake redis instance.
    :param client: client fixture.
    """
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('set_redis_value')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_query')
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
    actual_value = await fake_redis.get(test_key)
    assert actual_value == test_val


@pytest.mark.anyio
async def test_getting_value(
    fastapi_app: FastAPI,
    fake_redis: FakeRedis,
    client: AsyncClient,
) -> None:
    """
    Tests that you can get value from redis by key.

    :param fastapi_app: current application fixture.
    :param fake_redis: fake redis instance.
    :param client: client fixture.
    """
    test_key = uuid.uuid4().hex
    test_val = uuid.uuid4().hex
    await fake_redis.set(test_key, test_val)

    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('get_redis_value')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_query')
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

