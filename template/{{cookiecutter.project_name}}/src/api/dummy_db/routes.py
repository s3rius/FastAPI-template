import uuid
from typing import Optional

from fastapi import APIRouter, Depends

from src.api.dummy_db.schema import (
    UpdateDummyModel,
    GetDummyResponse,
)
{% if cookiecutter.add_elastic_search == "True" -%}
from src.api.dummy_db.schema import DummyElasticResponse, ElasticAdd
from src.services.elastic.schema import ElasticFilterModel
{%else%}
from src.api.dummy_db.schema import BaseDummyModel
{% endif %}

from src.models import DummyDBModel
from src.services.db.session import Session, db_session

router = APIRouter()
URL_PREFIX = "/dummy_db_obj"


@router.put("/")
async def create_dummy(dummy_obj: {% if cookiecutter.add_elastic_search == "True" -%}ElasticAdd{% else %}BaseDummyModel{% endif %}, session: Session = Depends(db_session)) -> None:
    """
    Add dummy object in database.
    If you have elastic search feature enabled it will be added in your index.
    """
    {% if cookiecutter.add_elastic_search == "True" -%}
    insert_query = DummyDBModel.create(**dummy_obj.dict()).returning(DummyDBModel.id)
    model_id = await session.scalar(insert_query)
    await DummyDBModel.elastic_add(
        model_id=model_id,
        **dummy_obj.dict()
    )
    {% else %}
    await session.execute(DummyDBModel.create(**dummy_obj.dict()))
    {% endif %}

@router.post("/{dummy_id}")
async def update_dummy_model(
        dummy_id: uuid.UUID,
        new_values: UpdateDummyModel,
        session: Session = Depends(db_session)
) -> None:
    await session.execute(DummyDBModel.update(dummy_id, **new_values.dict()))
    {% if cookiecutter.add_elastic_search == "True" -%}
    await DummyDBModel.elastic_update(
        model_id=dummy_id,
        **new_values.dict(exclude_unset=True)
    )
    {% endif %}


@router.delete("/{dummy_id}")
async def delete_dummy_model(dummy_id: uuid.UUID, session: Session = Depends(db_session)) -> None:
    await session.execute(DummyDBModel.delete(dummy_id))
    {% if cookiecutter.add_elastic_search == "True" -%}
    await DummyDBModel.elastic_delete(model_id=dummy_id)
    {% endif %}


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

{% if cookiecutter.add_elastic_search == "True" -%}
@router.get("/elastic", response_model=DummyElasticResponse)
async def dummy_elastic_filter(query: ElasticFilterModel = Depends(ElasticFilterModel)) -> DummyElasticResponse:
    results = await DummyDBModel.elastic_filter(**query.dict())
    return DummyElasticResponse(
        results=results
    )
{% endif %}
