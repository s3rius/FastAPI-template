from pydantic import BaseModel

from pydantic import ConfigDict
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
    {%- endif %}
    name: str

    {%- if cookiecutter.db_info.name == "mongodb" %}
    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, document_id: ObjectId) -> str:
        """
        Validator that converts `ObjectId` to json serializable `str`.

        :param document_id: Bson Id for this document.
        :return: The converted str.
        """
        return str(document_id)
    {%- endif %}

    model_config = ConfigDict(from_attributes=True)

class DummyModelInputDTO(BaseModel):
    """DTO for creating new dummy model."""

    name: str
