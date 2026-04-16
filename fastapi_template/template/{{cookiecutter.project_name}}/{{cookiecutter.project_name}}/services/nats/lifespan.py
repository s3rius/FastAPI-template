from fastapi import FastAPI
import natsrpy
from {{cookiecutter.project_name}}.settings import settings


async def init_nats(app: FastAPI) -> None:  # pragma: no cover
    """
    Initialize nats.

    This function creates nats instance
    and makes initial connection to
    the cluster.

    :param app: current application.
    """
    app.state.nats = natsrpy.Nats(settings.nats_hosts)
    await app.state.nats.startup()


async def shutdown_nats(app: FastAPI) -> None:  # pragma: no cover
    """
    Shutdown nats client.

    This function closes all connections
    and sends all pending data to nats.

    :param app: current application.
    """
    await app.state.nats.shutdown()
