from pydantic import BaseModel

{%- if cookiecutter.pydanticv1 != "True" %}
from pydantic import ConfigDict

{%- endif %}
{%- if cookiecutter.db_info.name == "mongodb" %}
{%- if cookiecutter.pydanticv1 == "True" %}
from pydantic import validator, Field
{%- else %}
from pydantic import field_validator
{%- endif %}
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
    {%- if cookiecutter.pydanticv1 == "True" %}
    id: str = Field(alias="_id")
    {%- else %}
    id: str
    {%- endif %}
    {%- endif %}
    name: str

    {%- if cookiecutter.db_info.name == "mongodb" %}
    {%- if cookiecutter.pydanticv1 == "True" %}
    @validator("id", pre=True)
    {%- else %}
    @field_validator("id", mode="before")
    {%- endif %}
    @classmethod
    def parse_object_id(cls, document_id: ObjectId) -> str:
        """
        Validator that converts `ObjectId` to json serializable `str`.

        :param document_id: Bson Id for this document.
        :return: The converted str.
        """
        return str(document_id)
    {%- endif %}


    {%- if cookiecutter.pydanticv1 == "True" %}
    class Config:
        orm_mode = True
    {%- else %}
    model_config = ConfigDict(from_attributes=True)
    {%- endif %}

class DummyModelInputDTO(BaseModel):
    """DTO for creating new dummy model."""

    name: str
