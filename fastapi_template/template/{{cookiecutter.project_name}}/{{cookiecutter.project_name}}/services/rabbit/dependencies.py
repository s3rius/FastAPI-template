from aio_pika import Channel
from aio_pika.pool import Pool
from fastapi import Request

{%- if cookiecutter.enable_taskiq == "True" %}
from taskiq import TaskiqDepends

{%- endif %}


def get_rmq_channel_pool(request: Request {%- if cookiecutter.enable_taskiq == "True" %} = TaskiqDepends(){%- endif %}) -> Pool[Channel]:  # pragma: no cover
    """
    Get channel pool from the state.

    :param request: current request.
    :return: channel pool.
    """
    return request.app.state.rmq_channel_pool
