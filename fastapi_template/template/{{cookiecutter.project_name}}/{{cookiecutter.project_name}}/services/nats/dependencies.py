from fastapi import Request
from natsrpy import Nats

{%- if cookiecutter.enable_taskiq == "True" %}
from taskiq import TaskiqDepends
{%- endif %}


def get_nats(request: Request {%- if cookiecutter.enable_taskiq == "True" %} = TaskiqDepends(){%- endif %}) -> Nats:  # pragma: no cover
    """
    Returns nats instance.

    :param request: current request.
    :return: nats from the state.
    """
    return request.app.state.nats
