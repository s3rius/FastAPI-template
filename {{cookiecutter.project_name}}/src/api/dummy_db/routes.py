import uuid
from typing import Optional

from fastapi import APIRouter, Depends

from src.api.dummy_db.schema import (
    BaseDummyModel,
    UpdateDummyModel,
    GetDummyResponse
)
from src.models import DummyDBModel
from src.services.db.session import Session, db_session

router = APIRouter()
URL_PREFIX = "/dummy_db_obj"


@router.put("/")
async def create_dummy(dummy_obj: BaseDummyModel, session: Session = Depends(db_session)) -> None:
    await session.execute(DummyDBModel.create(**dummy_obj.dict()))


@router.post("/{dummy_id}")
async def update_dummy_model(
        dummy_id: uuid.UUID,
        new_values: UpdateDummyModel,
        session: Session = Depends(db_session)
) -> None:
    await session.execute(DummyDBModel.update(dummy_id, **new_values.dict()))


@router.delete("/{dummy_id}")
async def delete_dummy_model(dummy_id: uuid.UUID, session: Session = Depends(db_session)) -> None:
    await session.execute(DummyDBModel.delete(dummy_id))


@router.get("/", response_model=GetDummyResponse)
async def filter_dummy_models(
        dummy_id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        session: Session = Depends(db_session)
) -> GetDummyResponse:
    filter_query = DummyDBModel.filter(
        dummy_id=dummy_id,
        name=name,
        surname=surname
    )
    results = await session.fetchall(filter_query)
    return GetDummyResponse(
        results=results
    )
