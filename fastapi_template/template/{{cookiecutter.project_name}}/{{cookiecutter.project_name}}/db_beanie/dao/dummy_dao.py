from typing import List, Optional

from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel


class DummyDAO:
    """Class for accessing dummy table."""

    async def create_dummy_model(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        await DummyModel.insert_one(DummyModel(name=name))

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        return await DummyModel.find_all(skip=offset, limit=limit).to_list()

    async def filter(
        self,
        name: Optional[str] = None
    ) -> List[DummyModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        if name is None:
            return []
        return await DummyModel.find(DummyModel.name == name).to_list()

    async def delete_dummy_model_by_name(
        self,
        name: str,
    ) -> Optional[DummyModel]:
        """
        Delete a dummy model by name.

        :param name: name of dummy instance.
        :return: option of a dummy model.
        """
        res = await DummyModel.find_one(DummyModel.name == name)
        if res is None:
            return res
        await res.delete()
        return res
