import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker
from {{cookiecutter.project_name}}.settings import settings

{%- if cookiecutter.enable_redis == "True" %}
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

{%- endif %}

{%- if cookiecutter.enable_rmq == "True" %}
from taskiq_aio_pika import AioPikaBroker

{%- endif %}

{%- if cookiecutter.enable_redis == "True" %}
result_backend = RedisAsyncResultBackend(
    redis_url=str(settings.redis_url.with_path("/1")),
)
{%- endif %}


{%- if cookiecutter.enable_rmq == "True" %}
broker = AioPikaBroker(
    str(settings.rabbit_url),
){%- if cookiecutter.enable_redis == "True" %}.with_result_backend(result_backend){%- endif %}
{%- elif cookiecutter.enable_redis == "True" %}
broker = ListQueueBroker(
    str(settings.redis_url.with_path("/1")),
).with_result_backend(result_backend)
{%- else %}
broker = ZeroMQBroker()
{%- endif %}

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "{{cookiecutter.project_name}}.web.application:get_app",
)
