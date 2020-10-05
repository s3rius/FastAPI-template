from typing import Any, Dict, Optional

from pydantic import Field
from pydantic.main import BaseModel


class TestSettings(BaseModel):
    __test__ = False

    request_data: Dict[str, Any]
    response_code: Optional[int]
    response_json: Optional[Dict[Any, Any]] = Field(None)
    validation_data: Optional[Dict[Any, Any]] = Field(None)
