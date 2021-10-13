from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from {{cookiecutter.project_name}}.web.api.router import api_router
from {{cookiecutter.project_name}}.web.lifetime import shutdown, startup
from importlib import metadata

{%- if cookiecutter.orm == 'tortoise' %}
from tortoise.contrib.fastapi import register_tortoise
from {{cookiecutter.project_name}}.db.config import TORTOISE_CONFIG
{%- endif %}


{%- if cookiecutter.self_hosted_swagger == 'True' %}
from fastapi.staticfiles import StaticFiles
from pathlib import Path


APP_ROOT = Path(__file__).parent.parent
{%- endif %}


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="{{cookiecutter.project_name}}",
        description="{{cookiecutter.project_description}}",
        version=metadata.version("{{cookiecutter.project_name}}"),
        {%- if cookiecutter.self_hosted_swagger == 'True' %}
        docs_url=None,
        redoc_url=None,
        {% else %}
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        {%- endif %}
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router, prefix="/api")

    {%- if cookiecutter.self_hosted_swagger == 'True' %}
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static"
    )
    {% endif %}

    {%- if cookiecutter.orm == 'tortoise' %}
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
        {%- if cookiecutter.enable_migrations == "False" %}
        generate_schemas=True,
        {%- endif %}
    )
    {%- endif %}

    return app
