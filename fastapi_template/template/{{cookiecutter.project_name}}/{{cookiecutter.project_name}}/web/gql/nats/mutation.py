import strawberry
from strawberry.types import Info
from {{cookiecutter.project_name}}.web.gql.context import Context
from .schema import NatsMessageDTO


@strawberry.type
class Mutation:
    """Mutation for nats package."""

    @strawberry.mutation(description="Send message to Nats")
    async def publish_nats_message(
        self,
        message: NatsMessageDTO,
        info: Info[Context, None],
    ) -> None:
        """
        Sends a message to nats.

        :param message: message to publish.
        :param info: current context.
        """
        await info.context.nats.publish(
            message.subject,
            message.message,
        )

