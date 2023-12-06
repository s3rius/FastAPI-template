from psycopg_pool import AsyncConnectionPool
from typing import Any
from starlette.requests import Request

{%- if cookiecutter.enable_taskiq == "True" %}
from taskiq import TaskiqDepends

{%- endif %}

async def get_db_pool(request: Request {%- if cookiecutter.enable_taskiq == "True" %} = TaskiqDepends(){%- endif %}) -> AsyncConnectionPool[Any]:
    """
    Return database connections pool.

    :param request: current request.
    :returns: database connections pool.
    """
    return request.app.state.db_pool
