import strawberry
from strawberry.types import Info
from {{cookiecutter.project_name}}.db.dao.dummy_dao import DummyDAO
from {{cookiecutter.project_name}}.web.gql.context import Context


@strawberry.type
class Mutation:
    """Mutations for dummies."""

    @strawberry.mutation(description="Create dummy object in a database")
    async def create_dummy_model(
        self,
        {%- if cookiecutter.orm in ["sqlalchemy", "psycopg"] %}
        info: Info[Context, None],
        {%- endif %}
        name: str,
    ) -> str:
        """
        Creates dummy model in a database.

        {% if cookiecutter.orm in ["sqlalchemy", "psycopg"] -%}
        :param info: connection info.
        {% endif -%}
        :param name: name of a dummy.
        :return: name of a dummy model.
        """
        {%- if cookiecutter.orm == "sqlalchemy" %}
        dao = DummyDAO(info.context.db_connection)
        {%- elif cookiecutter.orm == "psycopg" %}
        dao = DummyDAO(info.context.db_pool)
        {%- else %}
        dao = DummyDAO()
        {%- endif %}
        await dao.create_dummy_model(name=name)
        return name
