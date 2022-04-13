from typing import Any, AsyncGenerator

from psycopg import AsyncConnection
from starlette.requests import Request


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncConnection[Any], None]:
    """
    Create and get database connection.

    :param request: current request.
    :yield: database connection.
    """
    async with request.app.state.db_pool.connection() as conn:
        try:
            yield conn
        except Exception:  # noqa: S110
            pass  # noqa: WPS420
