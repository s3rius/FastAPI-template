import strawberry


@strawberry.input
class KafkaMessageDTO:
    """Input type for kafka mutation."""

    topic: str
    message: str
