import strawberry


@strawberry.type
class DummyModelDTO:
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    id: int
    name: str
