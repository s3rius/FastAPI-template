import strawberry


@strawberry.type
class Query:
    """Echo query."""

    @strawberry.field(description="Echo query")
    def echo(self, message: str) -> str:
        """
        Sends echo message back to user.

        :param message: incoming message.
        :returns: same message as the incoming.
        """
        return message
