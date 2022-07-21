from psycopg_pool import AsyncConnectionPool
from starlette.requests import Request


async def get_db_pool(request: Request) -> AsyncConnectionPool:
    """
    Return database connections pool.

    :param request: current request.
    :returns: database connections pool.
    """
    return request.app.state.db_pool
