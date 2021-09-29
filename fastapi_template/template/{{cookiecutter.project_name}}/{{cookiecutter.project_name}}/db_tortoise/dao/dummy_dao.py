from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
from typing import List, Optional


class DummyDAO:
    """Class for accessing dummy table."""

    async def create_dummy_model(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        await DummyModel.create(name=name)

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        return (
            await DummyModel.all().offset(offset).limit(limit)
        )

    async def filter(self, name: Optional[str] = None) -> List[DummyModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = DummyModel.all()
        if name:
            query = query.filter(name=name)
        return await query
