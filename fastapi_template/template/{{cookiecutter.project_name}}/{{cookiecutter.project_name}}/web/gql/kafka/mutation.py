import strawberry
from strawberry.types import Info
from {{cookiecutter.project_name}}.web.gql.context import Context
from {{cookiecutter.project_name}}.web.gql.kafka.schema import KafkaMessageDTO


@strawberry.type
class Mutation:
    """Mutation for rabbit package."""

    @strawberry.mutation(description="Send message to Kafka")
    async def send_kafka_message(
        self, message: KafkaMessageDTO,
        info: Info[Context, None],
    ) -> None:
        """
        Sends a message in Kafka.

        :param message: message to publish.
        :param info: current context.
        """
        await info.context.kafka_producer.send(
            topic=message.topic,
            value=message.message.encode(),
        )

