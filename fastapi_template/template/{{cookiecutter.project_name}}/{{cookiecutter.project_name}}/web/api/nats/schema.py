from pydantic import BaseModel


class NatsMessage(BaseModel):
    """DTO for kafka messages."""

    subject: str
    message: str
