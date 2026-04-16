from fastapi import APIRouter, Depends
from {{cookiecutter.project_name}}.services.nats.dependencies import get_nats
from {{cookiecutter.project_name}}.web.api.nats.schema import NatsMessage
from natsrpy import Nats

router = APIRouter()


@router.post("/")
async def publish_nats_message(
    nats_message: NatsMessage,
    nats: Nats = Depends(get_nats),
) -> None:
    """
    Sends message to nats.

    :param nats: nats instance.
    :param nats_message: message to publish.
    """
    await nats.publish(nats_message.subject, nats_message.message)
