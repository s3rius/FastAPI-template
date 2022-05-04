from pydantic import BaseModel


class RMQMessageDTO(BaseModel):
    """DTO for publishing message in RabbitMQ."""

    exchange_name: str
    routing_key: str
    message: str
