from pydantic import BaseModel

{%- if cookiecutter.pydanticv1 != "True" %}
from pydantic import ConfigDict

{%- endif %}


class DummyModelDTO(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    id: int
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
