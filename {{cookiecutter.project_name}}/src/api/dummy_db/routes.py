import uuid
from typing import List, Optional

from fastapi import APIRouter

from src.api.dummy_db.schema import (
    BaseDummyModel,
    UpdateDummyModel,
    ReturnDummyModel
)
from src.models import DummyDBModel

router = APIRouter()
URL_PREFIX = "/dummy_db_obj"


@router.put("/")
async def create_dummy(dummy_obj: BaseDummyModel) -> None:
    await DummyDBModel.create(**dummy_obj.dict())


@router.post("/{dummy_id}")
async def update_dummy_model(dummy_id: uuid.UUID, new_values: UpdateDummyModel) -> None:
    await DummyDBModel.update(dummy_id, **new_values.dict())


@router.delete("/{dummy_id}")
async def delete_dummy_model(dummy_id: uuid.UUID) -> None:
    await DummyDBModel.delete(dummy_id)


@router.get("/", response_model=List[ReturnDummyModel])
async def filter_dummy_models(
        dummy_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        surname: Optional[str] = None
) -> List[DummyDBModel]:
    return await DummyDBModel.filter(
        dummy_id=dummy_id,
        name=name,
        surname=surname
    )
