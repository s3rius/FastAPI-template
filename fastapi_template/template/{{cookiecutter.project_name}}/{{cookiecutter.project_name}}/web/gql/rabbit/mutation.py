import strawberry
from aio_pika import Message
from strawberry.types import Info
from {{cookiecutter.project_name}}.web.gql.context import Context
from {{cookiecutter.project_name}}.web.gql.rabbit.schema import RabbitMessageDTO


@strawberry.type
class Mutation:
    """Mutation for rabbit package."""

    @strawberry.mutation(description="Send message to RabbitMQ")
    async def send_rabbit_message(
        self, message: RabbitMessageDTO, info: Info[Context, None]
    ) -> None:
        """
        Sends a message in RabbitMQ.

        :param message: message to publish.
        :param info: current context.
        """
        async with info.context.rabbit.acquire() as conn:
            exchange = await conn.declare_exchange(
                name=message.exchange_name,
                auto_delete=True,
            )
            await exchange.publish(
                message=Message(
                    body=message.message.encode("utf-8"),
                    content_encoding="utf-8",
                    content_type="text/plain",
                ),
                routing_key=message.routing_key,
            )
