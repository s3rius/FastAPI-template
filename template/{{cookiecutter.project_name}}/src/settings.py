from enum import Enum

from pydantic import BaseSettings, Field


class AppMode(Enum):
    DEV = "development"
    PROD = "production"


class Settings(BaseSettings):
    # Application settings
    fastapi_env: AppMode = Field(default=AppMode.PROD)
    log_level: str = Field(default="INFO")
    # Auxiliary database settings
    db_echo: bool = Field(default=False)
    db_driver: str = Field(default="postgresql")
    # Postgres connection settings
    postgres_db: str = Field(...)
    postgres_host: str = Field(...)
    postgres_port: str = Field(...)
    postgres_user: str = Field(...)
    postgres_password: str = Field(...)
    {% if cookiecutter.add_redis == "True" -%}
    # Redis connection settings
    redis_host: str = Field(...)
    redis_port: int = Field(default=6379)
    redis_password: str = Field(...)
    {% endif %}
    {% if cookiecutter.add_scheduler == "True" -%}
    schedule_timer: int = Field(default=20)
    {% endif %}
    # httpbin client settings
    httpbin_host: str = Field(default="https://httpbin.org/")
    {% if cookiecutter.add_elastic_search == "True" -%}
    elastic_host: str = Field(...)
    {% endif %}

    @property
    def is_dev(self) -> bool:
        return self.fastapi_env == AppMode.DEV


settings = Settings()