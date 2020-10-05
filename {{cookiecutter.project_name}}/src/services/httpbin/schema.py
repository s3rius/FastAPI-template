from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DummyHttpBinObj(BaseModel):
    id: int
    name: str
    surname: str


class HTTPBinResponse(BaseModel):
    args: Dict[str, Any]
    data: str
    files: Dict[str, Any]
    form: Dict[str, str]
    headers: Dict[str, str]
    json_data: Optional[Dict[str, Any]] = Field(alias="json")
    origin: str
    url: str
