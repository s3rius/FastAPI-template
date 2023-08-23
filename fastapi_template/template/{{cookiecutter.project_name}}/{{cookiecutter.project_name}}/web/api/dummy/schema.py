from pydantic import BaseModel

{%- if cookiecutter.pydanticv1 != "True" %}
from pydantic import ConfigDict

{%- endif %}
{%- if cookiecutter.db_info.name == "mongodb" %}
from pydantic import field_validator
from bson import ObjectId
{%- endif %}


class DummyModelDTO(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    {%- if cookiecutter.db_info.name != "mongodb" %}
    id: int
    {%- else %}
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, document_id: ObjectId) -> str:
        """
        Validator for turning an incoming `ObjectId` into a
        json serializable `str`.
        """
        return str(document_id)
    {%- endif %}
    name: str


    {%- if cookiecutter.pydanticv1 == "True" %}
    class Config:
        orm_mode = True
    {%- else %}
    model_config = ConfigDict(from_attributes=True)
    {%- endif %}

class DummyModelInputDTO(BaseModel):
    """DTO for creating new dummy model."""

    name: str
