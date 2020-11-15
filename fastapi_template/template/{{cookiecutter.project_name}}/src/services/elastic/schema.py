import uuid
from typing import Optional, List

from pydantic import Field, BaseModel


class ESReturnModel(BaseModel):
    id: uuid.UUID
    tags: Optional[List[str]]


class ElasticFilterModel(BaseModel):
    query: str = Field(default="")
    limit: int = Field(default=100, lt=400)
    offset: int = Field(default=0)
