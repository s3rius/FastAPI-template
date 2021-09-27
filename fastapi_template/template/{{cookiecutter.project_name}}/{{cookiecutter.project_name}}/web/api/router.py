from fastapi.routing import APIRouter

{%- if cookiecutter.enable_routers == "True" %}
from {{cookiecutter.project_name}}.web.api import echo
{%- if cookiecutter.db_info.name != "none" %}
{%- if cookiecutter.add_dummy == 'True' %}
from {{cookiecutter.project_name}}.web.api import dummy
{%- endif %}
{%- endif %}
{%- if cookiecutter.enable_redis == "True" %}
from {{cookiecutter.project_name}}.web.api import redis
{%- endif %}
{%- endif %}
{%- if cookiecutter.self_hosted_swagger == "True" %}
from {{cookiecutter.project_name}}.web.api import docs
{%- endif %}
from {{cookiecutter.project_name}}.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
{%- if cookiecutter.self_hosted_swagger == "True" %}
api_router.include_router(docs.router)
{%- endif %}
{%- if cookiecutter.enable_routers == "True" %}
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
{%- if cookiecutter.db_info.name != "none" %}
{%- if cookiecutter.add_dummy == 'True' %}
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
{%- endif %}
{%- endif %}
{%- if cookiecutter.enable_redis == "True" %}
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
{%- endif %}
{%- endif %}
