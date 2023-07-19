from aiokafka import AIOKafkaProducer
from fastapi import Request

{%- if cookiecutter.enable_taskiq == "True" %}
from taskiq import TaskiqDepends

{%- endif %}


def get_kafka_producer(request: Request {%- if cookiecutter.enable_taskiq == "True" %} = TaskiqDepends(){%- endif %}) -> AIOKafkaProducer:  # pragma: no cover
    """
    Returns kafka producer.

    :param request: current request.
    :return: kafka producer from the state.
    """
    return request.app.state.kafka_producer
