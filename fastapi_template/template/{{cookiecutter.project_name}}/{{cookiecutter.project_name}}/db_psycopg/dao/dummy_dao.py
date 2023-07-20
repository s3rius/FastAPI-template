from termios import OFDEL
from typing import Any, List, Optional

from fastapi import Depends
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool
from {{cookiecutter.project_name}}.db.dependencies import get_db_pool
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel


class DummyDAO:
    """Class for accessing dummy table."""

    def __init__(
        self,
        db_pool: AsyncConnectionPool = Depends(get_db_pool),
    ):
        self.db_pool = db_pool


    async def create_dummy_model(self, name: str) -> None:
        """
        Creates new dummy in a database.

        :param name: name of a dummy.
        """
        async with self.db_pool.connection() as connection:
            async with connection.cursor(binary=True) as cur:
                await cur.execute(
                    "INSERT INTO dummy (name) VALUES (%(name)s);",
                    params={
                        "name": name,
                    }
                )

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        async with self.db_pool.connection() as connection:
            async with connection.cursor(
                binary=True,
                row_factory=class_row(DummyModel)
            ) as cur:
                res = await cur.execute(
                    "SELECT id, name FROM dummy LIMIT %(limit)s OFFSET %(offset)s;",
                    params={
                        "limit": limit,
                        "offset": offset,
                    }
                )
                return await res.fetchall()

    async def filter(
        self,
        name: Optional[str] = None,
    ) -> List[DummyModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        async with self.db_pool.connection() as connection:
            async with connection.cursor(
                binary=True,
                row_factory=class_row(DummyModel)
            ) as cur:
                if name is not None:
                    res = await cur.execute(
                        "SELECT id, name FROM dummy WHERE name=%(name)s;",
                        params={
                            "name": name,
                        }
                    )
                else:
                    res = await cur.execute("SELECT id, name FROM dummy;")
                return await res.fetchall()
