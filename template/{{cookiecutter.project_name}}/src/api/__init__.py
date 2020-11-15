from fastapi import APIRouter

from src.api.httpbin import URL_PREFIX as httpbin_prefix
from src.api.httpbin import router as httpbin_router
{% if cookiecutter.add_redis == "True" -%}
from src.api.redis_api import URL_PREFIX as redis_prefix
from src.api.redis_api import router as redis_router
{% endif %}
{% if cookiecutter.add_dummy_model == "True" -%}
from src.api.dummy_db import URL_PREFIX as dummy_db_prefix
from src.api.dummy_db import router as dummy_db_router
{% endif %}

api_router = APIRouter()

api_router.include_router(
    router=httpbin_router, prefix=httpbin_prefix, tags=['HTTPBin']
)
{% if cookiecutter.add_redis == "True" -%}
api_router.include_router(
    router=redis_router, prefix=redis_prefix, tags=["Redis"]
)
{% endif %}
{% if cookiecutter.add_dummy_model == "True" -%}
api_router.include_router(
    router=dummy_db_router, prefix=dummy_db_prefix, tags=["Dummy db object"]
)
{% endif %}