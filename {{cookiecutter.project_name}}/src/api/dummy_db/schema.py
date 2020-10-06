import uuid
from typing import Optional

from pydantic import Field, BaseConfig
from pydantic.main import BaseModel


class BaseDummyModel(BaseModel):
    name: str
    surname: str


class ReturnDummyModel(BaseDummyModel):
    id: uuid.UUID

    class Config(BaseConfig):
        orm_mode = True


class UpdateDummyModel(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)


class DummyFiltersModel(BaseModel):
    dummy_id: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
