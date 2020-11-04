import uuid
from datetime import datetime
from typing import Optional, List

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


class UpdateDummyModel(BaseModel):
    name: Optional[str] = Field(default=None, example="New name")
    surname: Optional[str] = Field(default=None, example="New surname")


class DummyFiltersModel(BaseModel):
    dummy_id: Optional[uuid.UUID] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
