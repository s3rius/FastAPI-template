import strawberry
from strawberry.fastapi import GraphQLRouter
from {{cookiecutter.project_name}}.web.gql.context import Context, get_context

{%- if cookiecutter.enable_routers == "True" %}
from {{cookiecutter.project_name}}.web.gql import echo

{%- if cookiecutter.add_dummy == 'True' %}
from {{cookiecutter.project_name}}.web.gql import dummy

{%- endif %}
{%- if cookiecutter.enable_redis == "True" %}
from {{cookiecutter.project_name}}.web.gql import redis

{%- endif %}
{%- if cookiecutter.enable_rmq == "True" %}
from {{cookiecutter.project_name}}.web.gql import rabbit

{%- endif %}
{%- if cookiecutter.enable_kafka == "True" %}
from {{cookiecutter.project_name}}.web.gql import kafka

{%- endif %}

{%- endif %}

@strawberry.type
class Query(  # noqa: WPS215
    {%- if cookiecutter.enable_routers == "True" %}
    echo.Query,
    {%- if cookiecutter.add_dummy == 'True' %}
    dummy.Query,
    {%- endif %}
    {%- if cookiecutter.enable_redis == "True" %}
    redis.Query,
    {%- endif %}
    {%- endif %}
):
    """Main query."""


@strawberry.type
class Mutation(  # noqa: WPS215
    {%- if cookiecutter.enable_routers == "True" %}
    echo.Mutation,
    {%- if cookiecutter.add_dummy == 'True' %}
    dummy.Mutation,
    {%- endif %}
    {%- if cookiecutter.enable_redis == "True" %}
    redis.Mutation,
    {%- endif %}
    {%- if cookiecutter.enable_rmq == "True" %}
    rabbit.Mutation,
    {%- endif %}
    {%- if cookiecutter.enable_kafka == "True" %}
    kafka.Mutation,
    {%- endif %}
    {%- endif %}
):
    """Main mutation."""


schema = strawberry.Schema(
    Query,
    Mutation,
)

gql_router: GraphQLRouter[Context, None] = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context,
)
