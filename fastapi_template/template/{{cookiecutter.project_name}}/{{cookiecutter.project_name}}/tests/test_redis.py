import uuid
import fakeredis
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status
from fakeredis.aioredis import FakeRedis


@pytest.mark.asyncio
async def test_setting_value(
    fastapi_app: FastAPI,
    fake_redis: FakeRedis,
    client: TestClient,
) -> None:
    """
    Tests that you can set value in redis.

    :param fastapi_app: current application fixture.
    :param fake_redis: fake redis instance.
    :param client: client fixture.
    """
    url = fastapi_app.url_path_for('set_redis_value')
    test_key = uuid.uuid4().hex
    test_val = uuid.uuid4().hex
    response = client.put(url, json={
        "key": test_key,
        "value": test_val
    })
    assert response.status_code == status.HTTP_200_OK
    actual_value = await fake_redis.get(test_key)
    assert actual_value == test_val


@pytest.mark.asyncio
async def test_getting_value(
    fastapi_app: FastAPI,
    fake_redis: FakeRedis,
    client: TestClient,
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

    url = fastapi_app.url_path_for('get_redis_value')
    response = client.get(url, params={"key": test_key})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['key'] == test_key
    assert response.json()['value'] == test_val
