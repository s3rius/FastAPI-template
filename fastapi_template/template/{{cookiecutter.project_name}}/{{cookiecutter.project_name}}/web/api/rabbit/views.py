from aio_pika import Channel, Message
from aio_pika.pool import Pool
from fastapi import APIRouter, Depends
from {{cookiecutter.project_name}}.services.rabbit.dependencies import \
    get_rmq_channel_pool
from {{cookiecutter.project_name}}.web.api.rabbit.schema import RMQMessageDTO

router = APIRouter()


@router.post("/")
async def send_rabbit_message(
    message: RMQMessageDTO,
    pool: Pool[Channel] = Depends(get_rmq_channel_pool),
) -> None:
    """
    Posts a message in a rabbitMQ's exchange.

    :param message: message to publish to rabbitmq.
    :param pool: rabbitmq channel pool
    """
    async with pool.acquire() as conn:
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
