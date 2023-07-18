from psycopg_pool import AsyncConnectionPool
from starlette.requests import Request

{%- if cookiecutter.enable_taskiq == "True" %}
from taskiq import TaskiqDepends

{%- endif %}

async def get_db_pool(request: Request {%- if cookiecutter.enable_taskiq == "True" %} = TaskiqDepends(){%- endif %}) -> AsyncConnectionPool:
    """
    Return database connections pool.

    :param request: current request.
    :returns: database connections pool.
    """
    return request.app.state.db_pool
