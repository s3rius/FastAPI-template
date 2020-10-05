import warnings
from typing import Generator

import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from src.services.db import db_url

warnings.filterwarnings("ignore", category=DeprecationWarning)


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
def create_db() -> Generator[None, None, None]:
    prepare_db()
    yield
    drop_db()


@pytest.fixture(scope="function")
def app_fixture(create_db: None) -> TestClient:
    from src.server import app

    api_client = TestClient(app)

    return api_client


@pytest.fixture(scope="function")
def pg_conn() -> Connection:
    engine = create_engine(str(db_url), pool_size=0, echo=True)
    conn = engine.connect()

    yield conn

    conn.close()