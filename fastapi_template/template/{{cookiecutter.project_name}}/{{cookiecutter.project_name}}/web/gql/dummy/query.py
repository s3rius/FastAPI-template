from typing import List

import strawberry
from strawberry.types import Info
from {{cookiecutter.project_name}}.db.dao.dummy_dao import DummyDAO
from {{cookiecutter.project_name}}.web.gql.context import Context
from {{cookiecutter.project_name}}.web.gql.dummy.schema import DummyModelDTO


@strawberry.type
class Query:
    """Query to interact with dummies."""

    @strawberry.field(description="Get all dummies")
    async def get_dummy_models(
        self,
        {%- if cookiecutter.orm in ["sqlalchemy", "psycopg"] %}
        info: Info[Context, None],
        {%- endif %}
        limit: int = 15,
        offset: int = 0,
    ) -> List[DummyModelDTO]:
        """
        Retrieves all dummy objects from database.

        {% if cookiecutter.orm in ["sqlalchemy", "psycopg"] -%}
        :param info: connection info.
        {% endif -%}
        :param limit: limit of dummy objects, defaults to 10.
        :param offset: offset of dummy objects, defaults to 0.
        :return: list of dummy objects from database.
        """
        {%- if cookiecutter.orm == "sqlalchemy" %}
        dao = DummyDAO(info.context.db_connection)
        {%- elif cookiecutter.orm == "psycopg" %}
        dao = DummyDAO(info.context.db_pool)
        {%- else %}
        dao = DummyDAO()
        {%- endif %}
        return await dao.get_all_dummies(limit=limit, offset=offset)  # type: ignore
