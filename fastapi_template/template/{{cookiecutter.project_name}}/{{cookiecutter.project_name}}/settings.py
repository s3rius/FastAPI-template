from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    {%- if cookiecutter.db_info.name != "none" %}
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
    redis_host: str = "{{cookiecutter.project_name}}-redis"
    redis_port: int = 6379
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[int] = None
    {% endif %}

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
            scheme="{{cookiecutter.db_info.driver}}",
            {%- endif %}
            path=f"///{self.db_file}"
        )
        {%- else %}
        return URL.build(
            {%- if cookiecutter.orm == "sqlalchemy" %}
            scheme="{{cookiecutter.db_info.async_driver}}",
            {%- elif cookiecutter.orm == "tortoise" %}
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

    class Config:
        env_file = ".env"
        env_prefix = "{{cookiecutter.project_name | upper }}_"
        env_file_encoding = "utf-8"


settings = Settings()
