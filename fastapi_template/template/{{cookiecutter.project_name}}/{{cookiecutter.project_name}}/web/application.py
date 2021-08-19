from fastapi import FastAPI

from {{cookiecutter.project_name}}.web.api.router import api_router
from {{cookiecutter.project_name}}.web.lifetime import shutdown, startup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="{{cookiecutter.project_name}}",
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router, prefix="/api")

    return app
