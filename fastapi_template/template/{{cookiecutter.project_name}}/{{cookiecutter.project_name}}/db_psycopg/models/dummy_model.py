from pydantic import BaseModel


class DummyModel(BaseModel):
    """Dummy model for database."""

    id: int
    name: str
