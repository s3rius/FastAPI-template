from fastapi.routing import APIRouter

from {{cookiecutter.project_name}}.web.api import echo

{%- if cookiecutter.db_info.name != "none" %}
from {{cookiecutter.project_name}}.web.api import dummy
{%- endif %}
{%- if cookiecutter.enable_redis == "True" %}
from {{cookiecutter.project_name}}.web.api import redis
{%- endif %}

api_router = APIRouter()
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
{%- if cookiecutter.db_info.name != "none" %}
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
{%- endif %}
{%- if cookiecutter.enable_redis == "True" %}
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
{%- endif %}
