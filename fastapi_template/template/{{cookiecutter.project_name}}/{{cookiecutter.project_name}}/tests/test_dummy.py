import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from typing import Any
{%- if cookiecutter.orm == 'sqlalchemy' %}
from sqlalchemy.ext.asyncio import AsyncSession
{%- elif cookiecutter.orm == 'psycopg' %}
from psycopg.connection_async import AsyncConnection
{%- endif %}
from starlette import status
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
from {{cookiecutter.project_name}}.db.dao.dummy_dao import DummyDAO

@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    {%- if cookiecutter.orm == "sqlalchemy" %}
    dbsession: AsyncSession,
    {%- elif cookiecutter.orm == "psycopg" %}
    dbsession: AsyncConnection[Any],
    {%- endif %}
) -> None:
    """Tests dummy instance creation."""
    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('create_dummy_model')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_query')
    {%- endif %}
    test_name = uuid.uuid4().hex
    {%- if cookiecutter.api_type == 'rest' %}
    response = await client.put(url, json={
        "name": test_name
    })
    {%- elif cookiecutter.api_type == 'graphql' %}
    response = await client.post(
        url,
        json={
            "query": "mutation($name: String!){createDummyModel(name: $name)}",
            "variables": {"name": test_name},
        },
    )
    {%- endif %}
    assert response.status_code == status.HTTP_200_OK
    {%- if cookiecutter.orm in ["sqlalchemy", "psycopg"] %}
    dao = DummyDAO(dbsession)
    {%- elif cookiecutter.orm in ["tortoise", "ormar", "piccolo"] %}
    dao = DummyDAO()
    {%- endif %}
    instances = await dao.filter(name=test_name)
    assert instances[0].name == test_name


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    {%- if cookiecutter.orm == "sqlalchemy" %}
    dbsession: AsyncSession,
    {%- elif cookiecutter.orm == "psycopg" %}
    dbsession: AsyncConnection[Any],
    {%- endif %}
) -> None:
    """Tests dummy instance retrieval."""
    {%- if cookiecutter.orm in ["sqlalchemy", "psycopg"] %}
    dao = DummyDAO(dbsession)
    {%- elif cookiecutter.orm in ["tortoise", "ormar", "piccolo"] %}
    dao = DummyDAO()
    {%- endif %}
    test_name = uuid.uuid4().hex
    await dao.create_dummy_model(name=test_name)

    {%- if cookiecutter.api_type == 'rest' %}
    url = fastapi_app.url_path_for('get_dummy_models')
    {%- elif cookiecutter.api_type == 'graphql' %}
    url = fastapi_app.url_path_for('handle_http_query')
    {%- endif %}

    {%- if cookiecutter.api_type == 'rest' %}
    response = await client.get(url)
    dummies = response.json()
    {%- elif cookiecutter.api_type == 'graphql' %}
    response = await client.post(
        url,
        json={"query": "query{dumies:getDummyModels{id name}}"},
    )
    dummies = response.json()["data"]["dumies"]
    {%- endif %}

    assert response.status_code == status.HTTP_200_OK
    assert len(dummies) == 1
    assert dummies[0]['name'] == test_name
