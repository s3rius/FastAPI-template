import uuid
from typing import Optional

from pydantic import Field
{% if cookiecutter.pg_driver == "aiopg" -%}
from pydantic import BaseConfig
{% endif %}
from pydantic.main import BaseModel


class BaseDummyModel(BaseModel):
    name: str
    surname: str


class ReturnDummyModel(BaseDummyModel):
    id: uuid.UUID

    {% if cookiecutter.pg_driver == "aiopg" -%}
    class Config(BaseConfig):
        orm_mode = True
    {% endif %}


class UpdateDummyModel(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)


class DummyFiltersModel(BaseModel):
    dummy_id: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
