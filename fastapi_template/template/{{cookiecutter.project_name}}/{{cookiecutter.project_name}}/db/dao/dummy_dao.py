from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncScalarResult, AsyncSession

from {{cookiecutter.project_name}}.db.dependencies import get_db_session
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel


class DummyDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_dummy_model(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(DummyModel(name=name))

    async def get_all_dummies(self, limit: int, offset: int) -> AsyncScalarResult:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_stream = await self.session.stream(
            select(DummyModel).limit(limit).offset(offset),
        )

        return raw_stream.scalars()
