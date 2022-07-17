from psycopg_pool import ConnectionPool
from starlette.requests import Request


async def get_db_pool(request: Request) -> ConnectionPool:
    """
    Return database connections pool.

    :param request: current request.
    :returns: database connections pool.
    """
    return request.app.state.db_pool
