from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from {{cookiecutter.project_name}}.db.dao.dummy_dao import DummyDAO
from {{cookiecutter.project_name}}.db.models.dummy_model import DummyModel
from {{cookiecutter.project_name}}.web.api.dummy.schema import (DummyModelDTO,
                                                                DummyModelInputDTO)

router = APIRouter()


@router.get("/", response_model=List[DummyModelDTO])
async def get_dummy_models(
    limit: int = 10,
    offset: int = 0,
    dummy_dao: DummyDAO = Depends(),
) -> List[DummyModel]:
    """
    Retrieve all dummy objects from the database.

    :param limit: limit of dummy objects, defaults to 10.
    :param offset: offset of dummy objects, defaults to 0.
{%- if cookiecutter.db_info.name != "mongodb" %}
    :param dummy_dao: DAO for dummy models.
{%- endif %}
    :return: list of dummy objects from database.
    """
    return await dummy_dao.get_all_dummies(limit=limit, offset=offset)


@router.put("/")
async def create_dummy_model(
    new_dummy_object: DummyModelInputDTO,
    dummy_dao: DummyDAO = Depends(),
) -> None:
    """
    Creates dummy model in the database.

    :param new_dummy_object: new dummy model item.
{%- if cookiecutter.db_info.name != "mongodb" %}
    :param dummy_dao: DAO for dummy models.
{%- endif %}
    """
    await dummy_dao.create_dummy_model(name=new_dummy_object.name)
