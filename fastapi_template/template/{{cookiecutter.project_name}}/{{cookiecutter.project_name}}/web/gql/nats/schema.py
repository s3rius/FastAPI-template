import strawberry


@strawberry.input
class NatsMessageDTO:
    """Input type for nats mutation."""

    subject: str
    message: str
