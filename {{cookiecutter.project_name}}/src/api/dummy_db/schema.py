import uuid
from datetime import datetime
from typing import Optional, List
from src.models.dummy_db_model import DummyElasticFilter
from pydantic import Field, BaseConfig
from pydantic.main import BaseModel


class BaseDummyModel(BaseModel):
    name: str = Field(example="Dummy name")
    surname: str = Field(example="Dummy surname")


class ReturnDummyModel(BaseDummyModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config(BaseConfig):
        orm_mode = True


class GetDummyResponse(BaseModel):
    results: List[ReturnDummyModel]

{% if cookiecutter.add_elastic_search == "True" -%}
class DummyElasticResponse(BaseModel):
    results: List[DummyElasticFilter]

class ElasticAdd(BaseDummyModel):
    tags: str = Field(default="")
{% endif %}

class UpdateDummyModel(BaseModel):
    name: Optional[str] = Field(default=None, example="New name")
    surname: Optional[str] = Field(default=None, example="New surname")
    {% if cookiecutter.add_elastic_search == "True" -%}
    tags: Optional[str] = Field(default=None, example="tag1,tag2")
    {% endif %}

class DummyFiltersModel(BaseModel):
    dummy_id: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
