import enum
from pathlib import Path
from tempfile import gettempdir
from typing import List, Optional

{%- if cookiecutter.pydanticv1 == "True" %}
from pydantic import BaseSettings

{%- else %}
from pydantic_settings import BaseSettings, SettingsConfigDict

{%- endif %}

from yarl import URL

TEMP_DIR = Path(gettempdir())

class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    {% if cookiecutter.db_info.name != "none" -%}

    # Variables for the database
    {%- if cookiecutter.db_info.name == "sqlite" %}
    db_file: Path = TEMP_DIR / "db.sqlite3"
    {%- else %}
    db_host: str = "localhost"
    db_port: int = {{cookiecutter.db_info.port}}
    db_user: str = "{{cookiecutter.project_name}}"
    db_pass: str = "{{cookiecutter.project_name}}"
    db_base: str = "{{cookiecutter.project_name}}"
    {%- endif %}
    db_echo: bool = False

    {%- endif %}


    {%- if cookiecutter.enable_redis == "True" %}

    # Variables for Redis
    redis_host: str = "{{cookiecutter.project_name}}-redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None

    {%- endif %}


    {%- if cookiecutter.enable_rmq == "True" %}

    # Variables for RabbitMQ
    rabbit_host: str = "{{cookiecutter.project_name}}-rmq"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    {%- endif %}


    {%- if cookiecutter.prometheus_enabled == "True" %}

    # This variable is used to define
    # multiproc_dir. It's required for [uvi|guni]corn projects.
    prometheus_dir: Path = TEMP_DIR / "prom"

    {%- endif %}


    {%- if cookiecutter.sentry_enabled == "True" %}

    # Sentry's configuration.
    sentry_dsn: Optional[str] = None
    sentry_sample_rate: float = 1.0

    {%- endif %}


    {%- if cookiecutter.otlp_enabled == "True" %}

    # Grpc endpoint for opentelemetry.
    # E.G. http://localhost:4317
    opentelemetry_endpoint: Optional[str] = None

    {%- endif %}

    {%- if cookiecutter.enable_kafka == "True" %}

    kafka_bootstrap_servers: List[str] = ["{{cookiecutter.project_name}}-kafka:9092"]

    {%- endif %}

    {%- if cookiecutter.db_info.name != "none" %}


    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        {%- if cookiecutter.db_info.name == "sqlite" %}
        return URL.build(
            {%- if cookiecutter.orm == "sqlalchemy" %}
            scheme="{{cookiecutter.db_info.async_driver}}",
            {%- elif cookiecutter.orm == "tortoise" %}
            scheme="{{cookiecutter.db_info.driver_short}}",
            {%- else %}
            scheme="{{cookiecutter.db_info.driver}}",
            {%- endif %}
            path=f"///{self.db_file}"
        )
        {%- else %}
        return URL.build(
            {%- if cookiecutter.orm == "sqlalchemy" %}
            scheme="{{cookiecutter.db_info.async_driver}}",
            {%- elif cookiecutter.orm == "tortoise" %}
            scheme="{{cookiecutter.db_info.driver_short}}",
            {%- else %}
            scheme="{{cookiecutter.db_info.driver}}",
            {%- endif %}
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )
        {%- endif %}
    {%- endif %}

    {%- if cookiecutter.enable_redis == "True" %}
    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )
    {%- endif %}

    {%- if cookiecutter.enable_rmq == "True" %}
    @property
    def rabbit_url(self) -> URL:
        """
        Assemble RabbitMQ URL from settings.

        :return: rabbit URL.
        """
        return URL.build(
            scheme="amqp",
            host=self.rabbit_host,
            port=self.rabbit_port,
            user=self.rabbit_user,
            password=self.rabbit_pass,
            path=self.rabbit_vhost,
        )
    {%- endif %}

    {%- if cookiecutter.pydanticv1 == "True" %}
    class Config:
        env_file = ".env"
        env_prefix = "{{cookiecutter.project_name | upper }}_"
        env_file_encoding = "utf-8"

    {%- else %}
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_prefix = "{{cookiecutter.project_name | upper }}_",
        env_file_encoding = "utf-8",
    )
    {%- endif %}



settings = Settings()
