from pydantic import BaseModel


class KafkaMessage(BaseModel):
    """DTO for kafka messages."""

    topic: str
    message: str
