import warnings
from typing import Generator

import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.exc import ProgrammingError

from src.services.db import db_url
from src.settings import settings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_engine() -> Engine:
    pg_db_url = make_url(
        str(URL(
            drivername=settings.db_driver,
            username=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            database="postgres",
        ))
    )
    engine = create_engine(str(pg_db_url))
    return engine


def run_psql_without_transaction(command: str) -> None:
    engine = get_engine()
    connection = engine.connect()
    connection.connection.set_isolation_level(0)
    connection.execute(command)
    connection.connection.set_isolation_level(1)
    connection.close()


@pytest.fixture(scope="session")
def create_database() -> None:
    try:
        run_psql_without_transaction(f"CREATE DATABASE {settings.postgres_db}")
    except ProgrammingError:
        pass


def prepare_db() -> None:
    alembic.config.main(
        [
            "--raiseerr",
            "upgrade",
            "head",
        ]
    )


def drop_db() -> None:
    alembic.config.main(
        [
            "--raiseerr",
            "downgrade",
            "base",
        ]
    )


@pytest.fixture(scope="function")
def create_db(create_database: None) -> Generator[None, None, None]:
    prepare_db()
    yield
    drop_db()


@pytest.fixture(scope="function")
def app_fixture(create_db: None) -> TestClient:
    from src.server import app

    api_client = TestClient(app)

    return api_client


@pytest.fixture(scope="function")
def pg_conn() -> Generator[Connection, None, None]:
    engine = create_engine(str(db_url), pool_size=0, echo=True)
    conn = engine.connect()

    yield conn

    conn.close()
