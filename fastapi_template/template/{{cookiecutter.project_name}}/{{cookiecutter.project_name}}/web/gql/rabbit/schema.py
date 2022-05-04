import strawberry


@strawberry.input
class RabbitMessageDTO:
    """Input type for rabbit mutation."""

    exchange_name: str
    routing_key: str
    message: str
