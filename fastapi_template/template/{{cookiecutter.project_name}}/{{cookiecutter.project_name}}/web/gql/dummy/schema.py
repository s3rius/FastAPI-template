import strawberry


@strawberry.type
class DummyModelDTO:
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
