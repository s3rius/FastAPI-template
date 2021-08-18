import asyncio
import sys
from typing import Any, Generator

import pytest

from {{cookiecutter.project_name}}.settings import settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of event loop for tests.

    This hack is required in order to get `dbsession` fixture to work.
    Because default fixture `event_loop` is function scoped,
    but dbsession requires session scoped `event_loop` fixture.

    :yields: event loop.
    """
    python_version = sys.version_info[:2]
    if sys.platform.startswith("win") and python_version >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def database_url() -> str:
    """
    Возвращает ссылку на тестовю базу данных.

    :return: URL.
    """
    return str(settings.db_url)


@pytest.fixture(scope="session")
def init_database() -> Any:
    """
    Create a database for tests.

    :return: ничего
    """
    from {{cookiecutter.project_name}}.db.meta import meta  # noqa: WPS433
    from {{cookiecutter.project_name}}.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    return meta.create_all
