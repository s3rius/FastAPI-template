from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

router = APIRouter()

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=request.app.openapi_url,
        title=request.app.title + " - Swagger UI",
        oauth2_redirect_url=request.url_for("swagger_ui_redirect"),
        swagger_js_url="/static/docs/swagger-ui-bundle.js",
        swagger_css_url="/static/docs/swagger-ui.css",
    )


@router.get("/swagger-redirect", include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
async def redoc_html(request: Request) -> HTMLResponse:
    return get_redoc_html(
        openapi_url=request.app.openapi_url,
        title=request.app.title + " - ReDoc",
        redoc_js_url="/static/docs/redoc.standalone.js",
    )
