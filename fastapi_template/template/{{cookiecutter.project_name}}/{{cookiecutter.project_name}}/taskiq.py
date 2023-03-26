from {{cookiecutter.project_name}}.settings import settings

import taskiq_fastapi
from taskiq import TaskiqState, ZeroMQBroker, InMemoryBroker, TaskiqEvents

{%- if cookiecutter.enable_redis == "True" %}
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
{%- endif %}

{%- if cookiecutter.enable_rmq == "True" %}
from taskiq_aio_pika import AioPikaBroker
{%- endif %}

{%- if cookiecutter.enable_loguru %}
from {{cookiecutter.project_name}}.logging import configure_logging
{%- endif %}


{%- if cookiecutter.enable_redis == "True" %}
result_backend = RedisAsyncResultBackend(
    redis_url=str(settings.redis_url.with_path("/1")),
)
{%- endif %}


{%- if cookiecutter.enable_rmq == "True" %}
broker = AioPikaBroker(str(settings.rabbit_url), {%- if cookiecutter.enable_redis == "True" %}result_backend=result_backend, {%- endif %})
{%- elif cookiecutter.enable_redis == "True" %}
broker = ListQueueBroker(str(settings.redis_url.with_path("/1")), result_backend=result_backend,)
{%- else %}
broker = ZeroMQBroker()
{%- endif %}

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(broker, "tkiqtest.web.application:get_app")
